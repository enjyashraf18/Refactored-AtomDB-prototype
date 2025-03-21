import json
import os
import shutil

from tinydb import Storage
from typing import Dict, Any
from zipfile import ZipFile, ZIP_DEFLATED
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ZipFileStorage(Storage):
    def __init__(self, filename):
        self.filename = filename
        self.temp_dir = f"temp_db_{os.path.basename(filename).replace('.zip', '')}"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.cache = self._load_cache()

    def _load_cache(self):
        try:
            if os.path.exists(self.filename):
                with ZipFile(self.filename, "r") as zip_file:
                    zip_file.extractall(self.temp_dir)
                    db_file = os.path.join(self.temp_dir, "db.json")
                    if os.path.exists(db_file):
                        with open(db_file, "r") as f:
                            return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
            return {}

    def read(self):
        return self.cache

    def write(self, data):
        self.cache = data
        try:
            db_file = os.path.join(self.temp_dir, "db.json")
            with open(db_file, "w") as f:
                json.dump(self.cache, f)
            with ZipFile(self.filename, "w", ZIP_DEFLATED) as zip_file:
                zip_file.write(db_file, "db.json")
        except Exception as e:
            logger.error(f"Error writing: {e}")

    def close(self):
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.error(f"error cleaning up temporary directory: {e}")

