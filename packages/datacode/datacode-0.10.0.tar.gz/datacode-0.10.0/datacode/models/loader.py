import uuid
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Dict, Optional, List

import pandas as pd
from datacode.models.column.column import Column
from pd_utils.optimize.load import read_file

from datacode.models.dtypes.datetime_type import DatetimeType

if TYPE_CHECKING:
    from datacode.models.source import DataSource
    from datacode.models.variables.variable import Variable

class DataLoader:

    def __init__(self, source: 'DataSource', read_file_kwargs: Optional[Dict[str, Any]] = None,
                 optimize_size: bool = False):
        if read_file_kwargs is None:
            read_file_kwargs = {}
        self.source = source
        self.optimize_size = optimize_size
        self.read_file_kwargs = read_file_kwargs

    def load(self) -> pd.DataFrame:
        df = self.read_file_into_df()
        self.duplicate_columns_for_calculations_assign_series(df)
        self.rename_columns(df)
        if self.optimize_size:
            df = self.optimize_df_size(df)
        self.assign_series_to_columns(df)
        df = self.try_to_calculate_variables(df)
        df = self.pre_transform_clean_up(df)
        df = self.apply_transforms(df)
        df = self.post_transform_clean_up(df)
        df = self.try_to_calculate_variables(df)
        self.assign_series_to_columns(df)
        self.drop_variables(df)

        return df

    def read_file_into_df(self) -> pd.DataFrame:
        if self.source.location is None:
            return pd.DataFrame()

        read_file_config = dict()

        # Set which columns to load
        if self.source.load_variables and self.source.columns:
            usecols = []
            for var in self.source.load_variables:
                for col in self.source.columns:
                    if col.variable.key == var.key:
                        # Got column matching the desired variable
                        usecols.append(col.load_key)  # add the original column name in the dataset to usecols
            read_file_config['usecols'] = usecols

        # Set the data types of the columns
        if self.source.columns:
            dtypes = {}
            datetime_dtypes = []  # pandas requires separate handling for datetime
            for col in self.source.columns:
                if col.dtype is not None:
                    if col.dtype.categorical:
                        dtypes[col.load_key] = 'category'
                    elif col.dtype == DatetimeType():
                        # Track datetime separately
                        datetime_dtypes.append(col.load_key)
                    else:
                        dtypes[col.load_key] = col.dtype.pd_class
            if dtypes:
                read_file_config['dtype'] = dtypes
            if datetime_dtypes:
                read_file_config['parse_dates'] = datetime_dtypes

        read_file_config.update(self.read_file_kwargs)

        return read_file(self.source.location, **read_file_config)

    def assign_series_to_columns(self, df: pd.DataFrame):
        if not self.source.columns:
            return
        for var in self.source.load_variables:
            if var.key not in self.source.col_var_keys:
                if var.calculation is None:
                    raise ValueError(f'passed variable {var} but not calculated and not '
                                     f'in columns {self.source.columns}')
                continue
            col = self.source.col_for(var)
            col.series = df[var.name]

    def duplicate_columns_for_calculations_assign_series(self, df: pd.DataFrame):
        if not self.source._columns_for_calculate or not self.source._vars_for_calculate:
            return

        # TODO [#39]: more efficient implementation of loading variables for calculations
        #
        # The `DataLoader` checks what variables are needed for calculations that are not
        # included in `load_variables`, and if it requires multiple transformations of
        # a variable, then it copies that series for as many transformations are needed.
        # It would be better to have an implementation that doesn't require carrying copies
        # through everything.

        load_var_keys = [var.key for var in self.source.load_variables]
        for col in self.source._columns_for_calculate:
            new_key = uuid.uuid4()  # temporary key for this variable
            # should get column which already has data for this variable
            existing_col = self.source.col_for(col.variable)
            df[new_key] = deepcopy(df[existing_col.load_key])
            col.load_key = new_key

    def optimize_df_size(self, df: pd.DataFrame) -> pd.DataFrame:
        # TODO [#17]: implement df size optimization
        #
        # Needs to be after adding data types to variables. Then can use data types to optimize
        raise NotImplementedError('implement df size optimization')

    def rename_columns(self, df: pd.DataFrame):
        from datacode.models.source import NoColumnForVariableException
        if not self.source.columns:
            return

        rename_dict = {}
        for variable in self.source._orig_load_variables:
            if variable.key not in self.source.col_var_keys:
                if variable.calculation is None:
                    raise ValueError(f'passed variable {variable} but not calculated and not '
                                     f'in columns {self.source.columns}')
                continue
            col = self.source.col_for(variable, orig_only=True)
            rename_dict[col.load_key] = variable.name
            col.variable = variable
        for variable in self.source._vars_for_calculate:
            try:
                col = self.source.col_for(variable, for_calculate_only=True)
                rename_dict[col.load_key] = variable.name
                col.variable = variable
            except NoColumnForVariableException:
                # Must be using a pre-existing column rather than a newly generated column, need to rename that instead
                col = self.source.col_for(variable, orig_only=True)
                rename_dict[col.load_key] = variable.name
                col.variable = variable
        df.rename(columns=rename_dict, inplace=True)

    def try_to_calculate_variables(self, df: pd.DataFrame):
        if not self.source.columns:
            return df

        # Create temporary source so that transform can have access to df and all columns with one object
        temp_source = deepcopy(self.source)
        temp_source.df = df
        temp_source.name = '_temp_source_for_transform'

        for variable in self.source.load_variables:
            if variable.key in self.source.col_var_keys:
                # Variable already exists in the data, either from original source or previously calculated
                continue

            if variable.calculation is None:
                raise ValueError(f'passed variable {variable} but not calculated and not '
                                 f'in columns {self.source.columns}')
            required_variables = variable.calculation.variables
            has_all_required_variables = True
            calc_with_cols = []
            for req_var in required_variables:
                if not has_all_required_variables:
                    break
                col = self.source.col_for(req_var)
                calc_with_cols.append(col)
                col_pre_applied_transform_keys = deepcopy(col.applied_transform_keys)
                for transform in req_var.applied_transforms:
                    # Need to make sure all the same transforms have been applied to
                    # the column before the calculation
                    if transform.key in col_pre_applied_transform_keys:
                        col_pre_applied_transform_keys.remove(transform.key)
                    else:
                        has_all_required_variables = False
                        break

            if has_all_required_variables:
                # Actually do calculation
                new_series = variable.calculation.func(calc_with_cols)
                new_series.name = variable.name
                # TODO [#34]: determine how to set index for columns from calculated variables
                new_col = Column(variable, dtype=str(new_series.dtype), series=new_series)
                temp_source.df[variable.name] = new_series
                temp_source.columns.append(new_col)
                temp_source = _apply_transforms_to_var(variable, new_col, temp_source)
                self.source.columns.append(new_col)

        return temp_source.df

    def apply_transforms(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.source.columns:
            return df

        # Create temporary source so that transform can have access to df and all columns with one object
        # TODO [#28]: don't copy df, use same df
        temp_source = deepcopy(self.source)
        temp_source.df = df
        temp_source.name = '_temp_source_for_transform'

        for var in self.source.load_variables:
            if not var.applied_transforms:
                continue
            if var.key not in self.source.col_var_keys:
                if var.calculation is None:
                    raise ValueError(f'passed variable {var} but not calculated and not '
                                     f'in columns {self.source.columns}')
                continue
            column = self.source.untransformed_col_for(var)
            temp_source = _apply_transforms_to_var(var, column, temp_source)
        return temp_source.df

    def drop_variables(self, df: pd.DataFrame):
        if not self.source._vars_for_calculate:
            # Only need to drop if extra variables were loaded for calculations
            return

        drop_names = [var.name for var in self.source._vars_for_calculate]
        df.drop(drop_names, axis=1, inplace=True)

    def pre_transform_clean_up(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def post_transform_clean_up(self, df: pd.DataFrame) -> pd.DataFrame:
        return df


def _apply_transforms_to_var(var: 'Variable', column: Column, source: 'DataSource') -> 'DataSource':
    col_pre_applied_transform_keys = deepcopy(column.applied_transform_keys)
    for transform in var.applied_transforms:
        if transform.key in col_pre_applied_transform_keys:
            # Transformation was already applied in the saved data source, skip this transformation
            # remove from applied transformations, because same transformation may be applied multiple times.
            # If desired transformation happens twice, and it is only once in the source column, will still
            # need to apply it once
            col_pre_applied_transform_keys.remove(transform.key)
            continue
        source = transform._apply_transform_for_column_and_variable_to_source(source, column, var)
        column.applied_transform_keys.append(transform.key)
        column.variable = var  # overwrite untransformed variable with transformed variable
    return source
