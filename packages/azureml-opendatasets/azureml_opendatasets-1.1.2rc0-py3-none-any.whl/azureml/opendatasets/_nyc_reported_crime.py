# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""New York crime."""

from .dataaccess._nyc_reported_crime_blob_info import NycReportedCrimeBlobInfo
from .dataaccess.blob_parquet_descriptor import BlobParquetDescriptor
from ._city_reported_crime import CityReportedCrime
from datetime import datetime
from dateutil import parser


class NycReportedCrime(CityReportedCrime):
    """New York city crime class."""

    default_start_date = parser.parse('2000-01-01')
    default_end_date = datetime.today()

    """const instance of blobInfo."""
    _blobInfo = NycReportedCrimeBlobInfo()

    data = BlobParquetDescriptor(_blobInfo)
