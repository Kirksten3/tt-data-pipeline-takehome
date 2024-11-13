import json
import os
from typing import Any, Dict
from google.cloud import storage


class GCS:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(bucket_name)

    def load_external_json(self, source_blob_name: str) -> Dict[str, Any]:
        blob = self.bucket.blob(source_blob_name)
        return json.loads(blob.download_as_text())


def load_file_or_backup(gcs_bucket: str, gcs_path: str, file_path: str):
    if os.getenv("DISABLE_GCS") == "true":
        with open(file_path) as file:
            return json.load(file)
    try:
        gcs = GCS(gcs_bucket)
        return gcs.load_external_json(gcs_path)
    except:
        with open(file_path) as file:
            return json.load(file)
