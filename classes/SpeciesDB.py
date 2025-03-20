import json
import numpy as np
from dataclasses import dataclass, asdict, field
from tinydb import TinyDB, Query
from tinydb.storages import Storage
from typing import Dict, Any, Optional
import logging
from zipfile import ZipFile, ZIP_DEFLATED
import os


class SpeciesDB:
    """Handles database operations for Species"""

    def __init__(self, datapath: str = "atomdb_data"):
        self.datapath = datapath
        self.db = None

    def dump(self):
        pass

    def load(self, elem: str, mult: int, nexc: int = 0, dataset: str = "default"):
        pass