import os
import shutil
from typing import Optional, Tuple, Any, Callable, Dict, Sequence, List

import pandas as pd
from pandas.testing import assert_frame_equal

from datacode.models.column.column import Column
from datacode.models.dtypes.str_type import StringType
from datacode.models.source import DataSource
from datacode.models.variables import Variable
from datacode.models.variables.expression import Expression
from datacode import Transform
from tests.utils import GENERATED_PATH


def transform_cell_data_func(col: Column, variable: Variable, cell: Any) -> Any:
    if isinstance(cell, str):
        return cell

    return cell + 1


def transform_series_data_func(col: Column, variable: Variable, series: pd.Series) -> pd.Series:
    return series + 1


def transform_dataframe_data_func(col: Column, variable: Variable, df: pd.DataFrame) -> pd.DataFrame:
    df[variable.name] = df[variable.name] + 1
    return df


def transform_source_data_func(col: Column, variable: Variable, source: DataSource) -> DataSource:
    # Extra unnecessary logic to access source.columns to test looking up columns
    cols = source.columns
    for this_col in cols:
        if not this_col.variable.key == col.variable.key:
            continue
        source.df[variable.name] = source.df[variable.name] + 1
    return source


def expression_series_func(cols: Sequence[Column]) -> pd.Series:
    return cols[0].series + cols[1].series


class SourceTest:
    test_df = pd.DataFrame(
        [
            (1, 2, 'd'),
            (3, 4, 'd'),
            (5, 6, 'e')
        ],
        columns=['a', 'b', 'c']
    )
    expect_loaded_df_rename_only = pd.DataFrame(
        [
            (1, 2, 'd'),
            (3, 4, 'd'),
            (5, 6, 'e')
        ],
        columns=['A', 'B', 'C'],
    )
    expect_loaded_df_rename_only_a_b = pd.DataFrame(
        [
            (1, 2,),
            (3, 4,),
            (5, 6,)
        ],
        columns=['A', 'B']
    )
    expect_loaded_df_with_transform = pd.DataFrame(
        [
            (2, 3, 'd'),
            (4, 5, 'd'),
            (6, 7, 'e')
        ],
        columns=['A_1', 'B_1', 'C']
    )
    expect_loaded_df_with_transform_only_a_b = pd.DataFrame(
        [
            (2, 3,),
            (4, 5,),
            (6, 7,)
        ],
        columns=['A_1', 'B_1']
    )
    expect_loaded_df_with_transform_and_a_pre_transformed = pd.DataFrame(
        [
            (1, 3, 'd'),
            (3, 5, 'd'),
            (5, 7, 'e')
        ],
        columns=['A_1', 'B_1', 'C']
    )
    expect_loaded_df_with_calculated = pd.DataFrame(
        [
            (1, 2, 'd', 3),
            (3, 4, 'd', 7),
            (5, 6, 'e', 11)
        ],
        columns=['A', 'B', 'C', 'D'],
    )
    expect_loaded_df_with_calculated_c_d_only = pd.DataFrame(
        [
            ('d', 3),
            ('d', 7),
            ('e', 11)
        ],
        columns=['C', 'D'],
    )
    expect_loaded_df_with_calculated_transformed = pd.DataFrame(
        [
            (1, 2, 'd', 4),
            (3, 4, 'd', 8),
            (5, 6, 'e', 12)
        ],
        columns=['A', 'B', 'C', 'D_1'],
    )
    expect_loaded_df_with_calculate_on_transformed_before_transform = pd.DataFrame(
        [
            (2, 3, 'd', 3),
            (4, 5, 'd', 7),
            (6, 7, 'e', 11)
        ],
        columns=['A_1', 'B_1', 'C', 'D'],
    )
    expect_loaded_df_with_calculate_on_transformed_after_transform = pd.DataFrame(
        [
            (2, 3, 'd', 5),
            (4, 5, 'd', 9),
            (6, 7, 'e', 13)
        ],
        columns=['A_1', 'B_1', 'C', 'D'],
    )
    expect_loaded_df_with_calculate_on_transformed_before_and_after_transform = pd.DataFrame(
        [
            (2, 3, 'd', 4),
            (4, 5, 'd', 8),
            (6, 7, 'e', 12)
        ],
        columns=['A_1', 'B_1', 'C', 'D'],
    )
    expect_loaded_df_categorical = expect_loaded_df_rename_only.copy()
    expect_loaded_df_categorical['C'] = expect_loaded_df_categorical['C'].astype('category')
    transform_name_func = lambda x: f'{x}_1'
    transform_cell = Transform('add_one_cell', transform_name_func, transform_cell_data_func, data_func_target='cell')
    transform_series = Transform('add_one_series', transform_name_func, transform_series_data_func, data_func_target='series')
    transform_dataframe = Transform('add_one_df', transform_name_func, transform_dataframe_data_func, data_func_target='dataframe')
    transform_source = Transform('add_one_source', transform_name_func, transform_source_data_func, data_func_target='source')
    csv_path = os.path.join(GENERATED_PATH, 'data.csv')

    def setup_method(self):
        os.makedirs(GENERATED_PATH)

    def teardown_method(self):
        shutil.rmtree(GENERATED_PATH)

    def create_source(self, **kwargs) -> DataSource:
        config_dict = dict(
            df=self.test_df,
            location=self.csv_path,
        )
        config_dict.update(kwargs)
        return DataSource(**config_dict)

    def get_transform(self, func_type: str) -> Transform:
        if func_type == 'cell':
            return self.transform_cell
        elif func_type == 'series':
            return self.transform_series
        elif func_type == 'dataframe':
            return self.transform_dataframe
        elif func_type == 'source':
            return self.transform_source
        else:
            raise ValueError(
                f'could not look up func_type {func_type}, should be one of cell, series, dataframe, source')

    def create_csv(self, df: Optional[pd.DataFrame] = None, **to_csv_kwargs):
        if df is None:
            df = self.test_df
        df.to_csv(self.csv_path, index=False, **to_csv_kwargs)

    def create_variables(self, transform_data: str = '', apply_transforms: bool = True) -> Tuple[Variable, Variable, Variable]:
        if transform_data:
            transform = self.get_transform(transform_data)
            transform_dict = dict(
                available_transforms=[transform],
            )
            if apply_transforms:
                transform_dict['applied_transforms'] = [transform]
        else:
            transform_dict = {}

        a = Variable('a', 'A', dtype='int', **transform_dict)
        b = Variable('b', 'B', dtype='int', **transform_dict)
        c = Variable('c', 'C', dtype='str')
        return a, b, c

    def create_columns(self, transform_data: str = '', apply_transforms: bool = True) -> List[Column]:
        a, b, c = self.create_variables(transform_data=transform_data, apply_transforms=apply_transforms)
        ac = Column(a, 'a')
        bc = Column(b, 'b')
        cc = Column(c, 'c')
        return [
            ac,
            bc,
            cc
        ]


class TestCreateSource(SourceTest):

    def test_create_source_from_df(self):
        ds = self.create_source(location=None)
        assert_frame_equal(ds.df, self.test_df)

    def test_create_source_from_file_path(self):
        self.create_csv()
        ds = self.create_source(df=None)
        assert_frame_equal(ds.df, self.test_df)

    def test_create_source_with_columns(self):
        all_cols = self.create_columns()
        ds = self.create_source(location=None, columns=all_cols)
        assert ds.columns == all_cols


class TestLoadSource(SourceTest):

    def test_load_with_columns(self):
        self.create_csv()
        all_cols = self.create_columns()
        ds = self.create_source(df=None, columns=all_cols)
        assert_frame_equal(ds.df, self.expect_loaded_df_rename_only)

    def test_load_with_columns_subset(self):
        self.create_csv()
        all_cols = self.create_columns()
        all_vars = self.create_variables()
        var_subset = [var for var in all_vars if var.key != 'c']
        ds = self.create_source(df=None, columns=all_cols, load_variables=var_subset)
        assert_frame_equal(ds.df, self.expect_loaded_df_rename_only_a_b)

    def test_with_with_columns_and_load_variables_with_transforms(self):
        self.create_csv()
        all_cols = self.create_columns(transform_data='cell', apply_transforms=False)
        a, b, c = self.create_variables(transform_data='cell', apply_transforms=False)
        load_variables = [
            a.add_one_cell(),
            b.add_one_cell(),
            c
        ]
        ds = self.create_source(df=None, columns=all_cols, load_variables=load_variables)
        assert_frame_equal(ds.df, self.expect_loaded_df_with_transform)

    def test_load_with_columns_and_transform_cell(self):
        self.create_csv()
        all_cols = self.create_columns(transform_data='cell')
        ds = self.create_source(df=None, columns=all_cols)
        assert_frame_equal(ds.df, self.expect_loaded_df_with_transform)

    def test_load_with_columns_and_transform_series(self):
        self.create_csv()
        all_cols = self.create_columns(transform_data='series')
        ds = self.create_source(df=None, columns=all_cols)
        assert_frame_equal(ds.df, self.expect_loaded_df_with_transform)

    def test_load_with_columns_and_transform_dataframe(self):
        self.create_csv()
        all_cols = self.create_columns(transform_data='dataframe')
        ds = self.create_source(df=None, columns=all_cols)
        assert_frame_equal(ds.df, self.expect_loaded_df_with_transform)

    def test_load_with_columns_and_transform_source(self):
        self.create_csv()
        all_cols = self.create_columns(transform_data='source')
        ds = self.create_source(df=None, columns=all_cols)
        assert_frame_equal(ds.df, self.expect_loaded_df_with_transform)

    def test_load_with_columns_transforms_and_pre_applied_transforms(self):
        self.create_csv()
        all_cols = self.create_columns(transform_data='cell')
        a, b, c = self.create_variables(transform_data='cell')
        all_cols[0] = Column(a, 'a', applied_transform_keys=['add_one_cell'])
        ds = self.create_source(df=None, columns=all_cols)
        assert_frame_equal(ds.df, self.expect_loaded_df_with_transform_and_a_pre_transformed)

    def test_load_with_categorical(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables()
        all_cols.append(Column(c, 'c', dtype=StringType(categorical=True)))
        ds = self.create_source(df=None, columns=all_cols)
        assert_frame_equal(ds.df, self.expect_loaded_df_categorical)

    def test_load_with_datetime(self):
        test_df = self.test_df.copy()
        test_df['d'] = pd.to_datetime('1/1/2000')
        self.create_csv(df=test_df)

        expect_df = self.expect_loaded_df_rename_only.copy()
        expect_df['Date'] = pd.to_datetime('1/1/2000')

        date_var = Variable('Date', dtype='datetime')
        date_col = Column(date_var, 'd')
        all_cols = self.create_columns()
        all_cols.append(date_col)

        ds = self.create_source(df=None, columns=all_cols)
        assert_frame_equal(ds.df, expect_df)

    def test_load_with_calculated_variable(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables()
        d = Variable('d', 'D', calculation=a + b)
        ds = self.create_source(df=None, columns=all_cols, load_variables=[a, b, c, d])
        assert_frame_equal(ds.df, self.expect_loaded_df_with_calculated)

    def test_load_with_calculated_variable_from_func(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables()
        expr = Expression([a, b], func=expression_series_func, summary='Add em up')
        d = Variable('d', 'D', calculation=expr)
        ds = self.create_source(df=None, columns=all_cols, load_variables=[a, b, c, d])
        assert_frame_equal(ds.df, self.expect_loaded_df_with_calculated)

    def test_load_with_calculated_transformed_variable(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables()
        tran = self.get_transform('cell')
        d = Variable('d', 'D', calculation=a + b, available_transforms=[tran])
        ds = self.create_source(df=None, columns=all_cols, load_variables=[a, b, c, d.add_one_cell()])
        assert_frame_equal(ds.df, self.expect_loaded_df_with_calculated_transformed)

    def test_load_with_calculate_on_transformed_after_transform(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables(transform_data='cell')
        d = Variable('d', 'D', calculation=a + b)
        ds = self.create_source(df=None, columns=all_cols, load_variables=[a, b, c, d])
        assert_frame_equal(ds.df, self.expect_loaded_df_with_calculate_on_transformed_after_transform)

    def test_load_with_calculate_on_transformed_before_transform(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables(transform_data='cell', apply_transforms=False)
        d = Variable('d', 'D', calculation=a + b)
        ds = self.create_source(df=None, columns=all_cols, load_variables=[a.add_one_cell(), b.add_one_cell(), c, d])
        assert_frame_equal(ds.df, self.expect_loaded_df_with_calculate_on_transformed_before_transform)

    def test_load_with_calculate_on_transformed_before_and_after_transform(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables(transform_data='cell', apply_transforms=False)
        d = Variable('d', 'D', calculation=a + b.add_one_cell())
        ds = self.create_source(df=None, columns=all_cols, load_variables=[a.add_one_cell(), b.add_one_cell(), c, d])
        assert_frame_equal(ds.df, self.expect_loaded_df_with_calculate_on_transformed_before_and_after_transform)

    def test_load_with_calculated_variable_using_non_passed_load_variables(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables()
        d = Variable('d', 'D', calculation=a + b)
        ds = self.create_source(df=None, columns=all_cols, load_variables=[c, d])
        assert_frame_equal(ds.df, self.expect_loaded_df_with_calculated_c_d_only)


# TODO [#49]: add test for save and load source after adding save functionality

class TestDunders(SourceTest):

    def test_str(self):
        source = self.create_source(location=None)
        print(source)


class TestTransform(SourceTest):

    def test_transform_existing_source(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables()
        orig_ds = self.create_source(df=None, columns=all_cols, load_variables=[a, b])
        all_ds = []
        all_ds.append(self.transform_cell.apply_to_source(orig_ds))
        all_ds.append(self.transform_series.apply_to_source(orig_ds))
        all_ds.append(self.transform_dataframe.apply_to_source(orig_ds))
        all_ds.append(self.transform_source.apply_to_source(orig_ds))
        for ds in all_ds:
            assert_frame_equal(ds.df, self.expect_loaded_df_with_transform_only_a_b)

    def test_transform_subset_existing_source(self):
        self.create_csv()
        all_cols = self.create_columns()
        a, b, c = self.create_variables()
        orig_ds = self.create_source(df=None, columns=all_cols)
        all_ds = []
        all_ds.append(self.transform_cell.apply_to_source(orig_ds, subset=[a, b]))
        all_ds.append(self.transform_series.apply_to_source(orig_ds, subset=[a, b]))
        all_ds.append(self.transform_dataframe.apply_to_source(orig_ds, subset=[a, b]))
        all_ds.append(self.transform_source.apply_to_source(orig_ds, subset=[a, b]))
        for ds in all_ds:
            assert_frame_equal(ds.df, self.expect_loaded_df_with_transform)
