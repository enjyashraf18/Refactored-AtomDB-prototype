import json
import os
from tinydb import Storage
from typing import Dict, Any, Optional
from zipfile import ZipFile, ZIP_DEFLATED


class ZipFileStorage(Storage):
    def __init__(self, filename: str):
        self.filename = filename




