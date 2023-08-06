# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""NOAA ISD weather."""

from datetime import datetime
from dateutil import parser
from pyspark.sql.functions import col, udf
from typing import List, Optional

from ._opendataset_factory import TabularOpenDatasetFactory
from .accessories.location_time_public_data import LocationTimePublicData
from .dataaccess._noaa_isd_weather_blob_info import NoaaIsdWeatherBlobInfo
from .dataaccess.blob_parquet_descriptor import BlobParquetDescriptor
from .dataaccess.dataset_partition_prep import prep_partition_year_month
from .dataaccess.pandas_data_load_limit import PandasDataLoadLimitToMonth
from .enrichers.common_weather_enricher import CommonWeatherEnricher
from .environ import SparkEnv, PandasEnv

from multimethods import multimethod


class NoaaIsdWeather(LocationTimePublicData, TabularOpenDatasetFactory):
    """Represents the  National Oceanic and Atmospheric Administration (NOAA) Integrated Surface Dataset (ISD).

    This dataset contains worldwide hourly weather history data (example: temperature, precipitation, wind)
    sourced from the National Oceanic and Atmospheric Administration (NOAA).
    For more information about this dataset, including column descriptions, different ways to access the dataset,
    and examples, see `NOAA Integrated Surface Data <https://azure.microsoft.com/services/open-datasets/
    catalog/noaa-integrated-surface-data/>`_ in the Microsoft Azure Open Datasets catalog.

    .. remarks::

        The example below shows how to use access the dataset.

        .. code-block:: python

            from azureml.opendatasets import NoaaIsdWeather
            from datetime import datetime
            from dateutil.relativedelta import relativedelta


            end_date = datetime.today()
            start_date = datetime.today() - relativedelta(months=1)
            isd = NoaaIsdWeather(start_date=start_date, end_date=end_date)
            isd_df = isd.to_pandas_dataframe()

        For backwards compatibility, the ``filter`` method can also be used to return a dataframe with results between
        a start and end date (inclusive). However, the pattern with ``to_pandas_dataframe`` is recommended.

        .. code-block:: python

            from azureml.opendatasets import NoaaIsdWeather
            from azureml.opendatasets import environ
            from dateutil import parser

            end_date = parser.parse('2018-06-06')
            start_date = parser.parse('2018-05-01')
            NoaaGfsWeather.env = environ.PandasEnv()
            isd_df = NoaaIsdWeather().filter(environ.PandasEnv(), start_date, end_date)

    :param start_data: The date at which to start loading data, inclusive. If None, the ``default_start_date``
        is used.
    :type start_data: datetime
    :param end_data: The date at which to end loading data, inclusive. If None, the ``default_end_date``
        is used.
    :type end_data: datetime
    :param cols: A list of columns names to load from the dataset. If None, all columns are loaded. For
        information on the available columns in this dataset, see `NOAA Integrated Surface
        Data <https://azure.microsoft.com/services/open-datasets/catalog/noaa-integrated-surface-data/>`__.
    :type cols: builtin.list[str]
    :param enable_telemetry: Whether to enable telemetry on this dataset.
        If not specified, telemetry is enabled.
    :type enable_telemetry: bool
    """

    default_start_date = parser.parse('2008-01-01')
    default_end_date = datetime.today()

    """const instance of blobInfo."""
    _blobInfo = NoaaIsdWeatherBlobInfo()

    data = BlobParquetDescriptor(_blobInfo)

    time_column_name = 'datetime'
    latitude_column_name = 'latitude'
    longitude_column_name = 'longitude'
    usaf_column_name = 'usaf'
    wban_column_name = 'wban'
    id = 'ID'

    mandatory_columns = [
        time_column_name,
        latitude_column_name,
        longitude_column_name,
        usaf_column_name,
        wban_column_name]

    partition_prep_func = prep_partition_year_month
    fine_grain_timestamp = time_column_name

    def __init__(
            self,
            start_date: datetime = default_start_date,
            end_date: datetime = default_end_date,
            cols: Optional[List[str]] = None,
            enable_telemetry: bool = True):
        """
        Initialize filtering fields.

        :param start_date: The start date you'd like to query inclusively.
        :type start_date: datetime
        :param end_date: The end date you'd like to query inclusively.
        :type end_date: datetime
        :param cols: A list of column names you'd like to retrieve. None will get all columns.
        :type cols: List[str]
        :param enable_telemetry: Indicates whether to enable telemetry, disabled for UT only.
        :type enable_telemetry: bool
        """
        self._registry_id = self._blobInfo.registry_id
        self.path = self._blobInfo.get_data_wasbs_path()
        self.start_date = start_date\
            if (self.default_start_date < start_date)\
            else self.default_start_date
        self.end_date = end_date\
            if (end_date is None or self.default_end_date > end_date)\
            else self.default_end_date
        super(NoaaIsdWeather, self).__init__(cols, enable_telemetry=enable_telemetry)
        if enable_telemetry:
            self.log_properties['StartDate'] = self.start_date.strftime("%Y-%m-%dT%H:%M:%S")\
                if self.start_date is not None else ''
            self.log_properties['EndDate'] = self.end_date.strftime("%Y-%m-%dT%H:%M:%S")\
                if self.end_date is not None else ''
            self.log_properties['Path'] = self.path

    @multimethod(SparkEnv, datetime, datetime)
    def filter(self, env, min_date, max_date):
        """Filter time.

        :param min_date: The min date.
        :type min_date: datetime
        :param max_date: The max date.
        :type min_date: datetime

        :return: The filtered data frame.
        """
        self.data = self.data.na.drop(how='all', subset=self.cols).na.drop(
            how='any', subset=[self.wban_column_name, self.usaf_column_name])

        # create unique id for weather stations, hardcoded due to id issue in weather dataset
        unique_id_udf = udf(lambda x, y: '-'.join([x, y]))
        self.data = self.data.withColumn(
            self.id, unique_id_udf(col(self.usaf_column_name), col(self.wban_column_name)))

        ds = super(NoaaIsdWeather, self).filter(env, min_date, max_date)
        return ds.select(self.selected_columns + [self.id])

    @multimethod(PandasEnv, datetime, datetime)
    def filter(self, env, min_date, max_date):
        """Filter time.

        :param min_date: The min date.
        :type min_date: datetime
        :param max_date: The max date.
        :type min_date: datetime

        :return: The filtered data frame.
        """
        ds = super(NoaaIsdWeather, self).filter(env, min_date, max_date)
        ds = ds.dropna(how='all', axis=0, subset=self.cols).dropna(
            how='any', axis=0, subset=[self.wban_column_name, self.usaf_column_name])

        # create unique id for weather stations, hardcoded due to id issue in weather dataset
        ds[self.id] = ds[self.usaf_column_name] + '-' + ds[self.wban_column_name]

        return ds[self.selected_columns + [self.id]]

    def _get_enricher(self, activity_logger):
        """Get enricher object.

        :param activity_logger: activity logger

        :return: enricher object
        """
        return CommonWeatherEnricher(self, enable_telemetry=self.enable_telemetry)

    def get_pandas_limit(self):
        """Get instance of pandas data load limit class."""
        return PandasDataLoadLimitToMonth(self.start_date, self.end_date)

    def _to_spark_dataframe(self, activity_logger):
        """To spark dataframe.

        :param activity_logger: activity logger

        :return: SPARK dataframe
        """
        descriptor = BlobParquetDescriptor(self._blobInfo)
        return descriptor.get_spark_dataframe(self)

    def _to_pandas_dataframe(self, activity_logger):
        """
        Get pandas dataframe.

        :param activity_logger: activity logger

        :return: Pandas dataframe based on its own filters.
        :rtype: pandas.DataFrame
        """
        descriptor = BlobParquetDescriptor(self._blobInfo)
        return descriptor.get_pandas_dataframe(self)
