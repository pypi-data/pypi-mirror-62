# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Blob info of NYC Taxi FHV trip data."""

from .base_blob_info import BaseBlobInfo


class NycTlcFhvBlobInfo(BaseBlobInfo):
    """Blob info of NYC Taxi FHV trip data."""

    def __init__(self):
        """Initialize Blob Info."""
        self.registry_id = 'nyc_tlc_fhv'
        self.blob_account_name = 'azureopendatastorage'
        self.blob_container_name = "nyctlc"
        self.blob_relative_path = "fhv/"
        self.blob_sas_token = (
            r"?st=2019-03-04T01%3A15%3A47Z&se=2169-01-01T01%3A15%3A00Z&sp=rl&sv=2018-03-28&sr=c"
            # [SuppressMessage("Microsoft.Security", "CS002:SecretInNextLine", Justification="Offline sas token")]
            r"&sig=Ib7t3BIk9K1HDbnm7JbTrk98aiOoTQdgsp3qK%2BIwK1c%3D")
