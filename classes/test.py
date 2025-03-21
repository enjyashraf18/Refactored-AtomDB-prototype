from tinydb import TinyDB, Query
from tinydb.table import Document
from dataclasses import fields
import json

import gzip
import json
import numpy as np
import yaml
from dataclasses import dataclass, asdict, field
from tinydb import TinyDB, Query
from tinydb.storages import Storage
from typing import Dict, Any, Optional
import logging

class Species(Document):
    """
    Species is a class for representing atomic and ionic species.
    """

    def __init__(self, dataset, fields, spinpol=1, doc_id=None):
        super().__init__(value=fields, doc_id=doc_id)
        self._dataset = dataset.lower()
        self._spinpol = spinpol
        self._fields = fields

        # Instead of manually assigning each field (for ex: self.elem = fields["elem"])
        for field_name, value in fields.items():
            setattr(self, field_name, value)

    # def to_dict(self):
    #     # return asdict(self._data)
    #     return self._fields
    """No Conversion Required anymore"""

    def get_data(self):
        """simply returns self._fields dict"""
        return self._fields

    @classmethod
    def from_dict(cls, dataset, data):
        """create a species instance from a dictionary"""
        return cls(dataset, data)

    def to_json(self):
        """convert the species instance to a JSON string"""
        return json.dumps(self.to_dict(), indent=4)


    @property
    def dataset(self):
        """return the dataset name"""
        return self._dataset



    @property
    def charge(self):
        """compute the charge of the species"""
        return self._fields["atnum"] - self._fields["nelec"]

    @property
    def spinpol(self):
        """get the spin polarization direction."""
        return self._spinpol

    @spinpol.setter
    def spinpol(self, value):
        """Set the spin polarization direction."""
        if value not in (1, -1):
            raise ValueError("Spin polarization must be +1 or -1.")
        self._spinpol = value


def dump(species, datapath="atomdb_data"):
    db = TinyDB(f"{datapath}/{species.dataset}.json")
    db.insert(species.get_data())
    print(f"db inserted {db} ")


def load(elem, mult, nexc=0, dataset="default", datapath="atomdb_data"):
    db = TinyDB(f"{datapath}/{dataset}.json")
    print("Database contents:", db.all())
    query = Query()
    result = db.search(
        (query.elem == elem)
        & (query.mult == mult)
        & (query.nexc == nexc)
    )
    print(f" load result {result}")
    if result:
        return Species.from_dict(dataset, result[0])
    else:
        raise ValueError("Species not found in the database.")

fields = {
        "elem": "H",
        "atnum": 1,
        "nelec": 1,
        "nspin": 0,
        "nexc": 0,
        "energy": -0.5,
        "mult": 2,
    }
species = Species("default", fields)
dump(species)
loaded_species = load("H", 2, 0)
print(f" load result {loaded_species}")



# import json
# import os
# from tinydb import Storage
# from typing import Dict, Any, Optional
# from zipfile import ZipFile, ZIP_DEFLATED
# import logging
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# class ZipFileStorage(Storage):
#     def __init__(self, filename):
#         self.filename = filename
#         self.temp_dir = f"temp_db_{os.path.basename(filename).replace('.zip', '')}"  # Unique temp dir per shard
#         os.makedirs(self.temp_dir, exist_ok=True)
#         self.cache = self._load_cache()  # Load cache on init
#
#
#     def _load_cache(self):
#         # Load initial cache from disk
#         try:
#             if os.path.exists(self.filename):
#                 with ZipFile(self.filename, "r") as zip_file:
#                     zip_file.extractall(self.temp_dir)
#                     db_file = os.path.join(self.temp_dir, "db.json")
#                     if os.path.exists(db_file):
#                         with open(db_file, "r") as f:
#                             return json.load(f)
#             return {}
#         except Exception as e:
#             logger.error(f"Error loading cache: {e}")
#             return {}
#
#     def read(self):
#         """Return the cached data"""
#         return self.cache
#
#     def write(self, data):
#         """update cache and disk immediately"""
#         self.cache = data
#         try:
#             db_file = os.path.join(self.temp_dir, "db.json")
#             with open(db_file, "w") as f:
#                 json.dump(self.cache, f)
#             with ZipFile(self.filename, "w", ZIP_DEFLATED) as zip_file:
#                 zip_file.write(db_file, "db.json")
#         except Exception as e:
#             logger.error(f"Error writing to ZipFile: {e}")
#
#     def close(self):
#         """clean up temporary dict"""
#         try:
#             import shutil
#             shutil.rmtree(self.temp_dir)
#         except Exception as e:
#             logger.error(f"Error cleaning up temporary directory: {e}")
#
#
#
#