from functools import partial
from typing import List, Callable

from datacode.models.pipeline.base import DataPipeline
from datacode.models.source import DataSource
from datacode.models.merge import MergeOptions, LastMergeFinishedException, DataMerge
from datacode.models.types import DataSourceOrPipeline, DataSourcesOrPipelines, MergeOptionsList, DataMerges


class DataMergePipeline(DataPipeline):
    """
    Handles data pipelines involving merges between two or more sources or pipelines
    """

    def __init__(self, data_sources: DataSourcesOrPipelines =None, merge_options_list: MergeOptionsList =None,
                 outpath=None, post_merge_cleanup_func=None, name: str=None, cleanup_kwargs: dict=None):

        if cleanup_kwargs is None:
            cleanup_kwargs = {}

        self.merge_options_list = merge_options_list
        self._merge_index = 0
        self._set_cleanup_func(post_merge_cleanup_func, **cleanup_kwargs)
        self.cleanup_kwargs = cleanup_kwargs

        super().__init__(data_sources=data_sources, name=name, outpath=outpath)

    def execute(self):
        while True:
            try:
                self.next_merge()
            except LastMergeFinishedException:
                break

        if self.has_post_merge_cleanup_func:
            self.df = self.post_merge_cleanup_func(self.df)
        self.output()

        return self.df

    def next_merge(self):
        # On first merge, set df
        if self._merge_index == 0:
            self._set_df_from_first_merge()

        self._merge()

    def summary(self, *summary_args, summary_method: str=None, summary_function: Callable=None,
                             summary_attr: str=None, **summary_method_kwargs):
        for merge in self.merges:
            merge.summary(
                *summary_args,
                summary_method=summary_method,
                summary_function=summary_function,
                summary_attr=summary_attr,
                **summary_method_kwargs
            )

    def describe(self):
        for merge in self.merges:
            merge.describe()

    def _output(self, outpath=None):
        self.df.to_csv(outpath, index=False, encoding='utf8')

    def _merge(self):
        try:
            print(f'Now running merge {self._merge_index + 1}: {self.merges[self._merge_index]}')
        except IndexError:
            raise LastMergeFinishedException

        self.merges[self._merge_index].merge()

        # Set current df to result of merge
        self.df = self.merges[self._merge_index].result.df

        self._merge_index += 1

        # TODO [#5]: add output considering path in merge options

    @property
    def merges(self):
        try:
            return self._merges
        except AttributeError:
            self._set_merges()

        return self._merges

    # Following properties exist to recreate merges if data sources or merge options are overridden
    # by user

    @property
    def data_sources(self):
        return self._data_sources

    @data_sources.setter
    def data_sources(self, data_sources: DataSourcesOrPipelines):
        self._data_sources = data_sources
        # only set merges if previously set. otherwise no need to worry about updating cached result
        if hasattr(self, '_merges'):
            self._set_merges()

    @property
    def merge_options_list(self):
        return self._merge_options_list

    @merge_options_list.setter
    def merge_options_list(self, merge_options_list: MergeOptionsList):
        self._merge_options_list = merge_options_list
        # only set merges if previously set. otherwise no need to worry about updating cached result
        if hasattr(self, '_merges'):
            self._set_merges()

    def _set_merges(self):
        self._merges = self._create_merges(self.data_sources, self.merge_options_list)

    def _create_merges(self, data_sources: DataSourcesOrPipelines, merge_options_list: MergeOptionsList):
        merges = _get_merges(data_sources[0], data_sources[1], merge_options_list[0])
        if len(merge_options_list) == 1:
            return merges

        for i, merge_options in enumerate(merge_options_list[1:]):
            merges += _get_merges(merges[-1].result, data_sources[i + 2], merge_options)

        return merges

    def _set_df_from_first_merge(self):
        self.df = self.merges[0].data_sources[0].df

    def _set_cleanup_func(self, post_merge_cleanup_func, **cleanup_kwargs):
        if post_merge_cleanup_func is not None:
            self.has_post_merge_cleanup_func = True
            self.post_merge_cleanup_func = partial(post_merge_cleanup_func, **cleanup_kwargs)
        else:
            self.has_post_merge_cleanup_func = False


def _get_merges(data_source_1: DataSourceOrPipeline, data_source_2: DataSourceOrPipeline,
                merge_options: MergeOptions) -> DataMerges:
    """
    Creates a list of DataMerge objects from a paring of two DataSource objects, a DataSource and a DataMergePipeline,
    or two DataMergePipeline objects.
    :param data_source_1: DataSource or DataMergePipeline
    :param data_source_2: DataSource or DataMergePipeline
    :param merge_options: MergeOptions
    :return: list of DataMerge objects
    """
    merges: DataMerges = []
    final_merge_sources: List[DataSource] = []
    # Add any pipeline merges first, as the results from the pipeline must be ready before we can merge the results
    # to other data sources or pipeline results
    if _is_data_pipeline(data_source_1):
        merges += data_source_1.merges  # type: ignore
        pipeline_1_result = data_source_1.merges[-1].result  # type: ignore
        final_merge_sources.append(pipeline_1_result) # result of first pipeline will be first source in final merge

    if _is_data_pipeline(data_source_2):
        merges += data_source_2.merges  # type: ignore
        # result of second pipeline will be second source in final merge
        pipeline_2_result = data_source_2.merges[-1].result # type: ignore

    if not _is_data_pipeline(data_source_1):
        final_merge_sources.append(data_source_1)  # type: ignore

    # Now final merge source 1 is filled, may add 2
    if _is_data_pipeline(data_source_2):
        final_merge_sources.append(pipeline_2_result)
    elif not _is_data_pipeline(data_source_2):
        final_merge_sources.append(data_source_2) # type: ignore

    # Add last (or only) merge
    merges.append(DataMerge(final_merge_sources, merge_options))

    return merges


def _is_data_pipeline(obj) -> bool:
    return hasattr(obj, 'data_sources') and hasattr(obj, 'merge_options_list')