# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Diabetes data."""

from azureml.core import Dataset
from azureml.data import TabularDataset
from azureml.telemetry.activity import ActivityType

from ._utils.telemetry_utils import get_run_common_properties
from .accessories.public_data_telemetry import _PublicDataTelemetry
from .dataaccess._diabetes_blob_info import DiabetesBlobInfo


class Diabetes:
    """Represents the Sample Diabetes public dataset.

    The Diabetes dataset has 442 samples with 10 features, making it ideal for getting started with machine
    learning algorithms. For more information about this dataset, including column descriptions, different
    ways to access the dataset, and examples, see `Sample: Diabetes <https://azure.microsoft.com/
    services/open-datasets/catalog/sample-diabetes/>`_ in the Microsoft Azure Open Datasets catalog.
    """

    _blobInfo = DiabetesBlobInfo()

    @staticmethod
    def _get_logger_prop(blobInfo: DiabetesBlobInfo):
        log_properties = get_run_common_properties()
        log_properties['RegistryId'] = blobInfo.registry_id
        log_properties['Path'] = blobInfo.get_data_wasbs_path()
        return log_properties

    @staticmethod
    def get_tabular_dataset(
            enable_telemetry: bool = True) -> TabularDataset:
        """Return a :class:`azureml.data.TabularDataset` containing the data.

        :return: A tabular dataset.
        :rtype: azureml.data.TabularDataset
        """
        _url_path = Diabetes._blobInfo.get_url()
        if enable_telemetry:
            log_properties = Diabetes._get_logger_prop(Diabetes._blobInfo)
            log_properties['ActivityType'] = ActivityType.PUBLICAPI
            _PublicDataTelemetry.log_event('get_tabular_dataset', **log_properties)
            return Dataset.Tabular.from_parquet_files(path=_url_path)
        else:
            return Dataset.Tabular.from_parquet_files(path=_url_path)
