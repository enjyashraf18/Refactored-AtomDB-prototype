import json
import os
from tinydb import TinyDB, Query, Storage
from tinydb.storages import JSONStorage
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional
from zipfile import ZipFile, ZIP_DEFLATED
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom ZipFileStorage with write-through caching
class ZipFileStorage(Storage):
    def __init__(self, filename: str):
        self.filename = filename
        self.temp_dir = f"temp_db_{os.path.basename(filename).replace('.zip', '')}"  # Unique temp dir per shard
        os.makedirs(self.temp_dir, exist_ok=True)
        self.cache = self._load_cache()  # Load cache on init

    def _load_cache(self) -> Dict:
        """Load initial cache from disk."""
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
            logger.error(f"Error loading cache from ZipFile: {e}")
            return {}

    def read(self) -> Optional[Dict]:
        """Return the cached data."""
        return self.cache

    def write(self, data: Dict) -> None:
        """Write-through: update cache and disk immediately."""
        self.cache = data  # Update in-memory cache
        try:
            db_file = os.path.join(self.temp_dir, "db.json")
            with open(db_file, "w") as f:
                json.dump(self.cache, f)  # Write to temp file
            with ZipFile(self.filename, "w", ZIP_DEFLATED) as zip_file:
                zip_file.write(db_file, "db.json")  # Update ZIP with only db.json
        except Exception as e:
            logger.error(f"Error writing to ZipFile: {e}")

    def close(self) -> None:
        """Clean up temporary directory."""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.error(f"Error cleaning up temporary directory: {e}")

# Species class (unchanged)
@dataclass
class Species:
    dataset: str
    elem: str
    atnum: int
    nelec: int
    nspin: int
    nexc: int
    energy: float
    mult: int
    spinpol: int = field(default=1)
    doc_id: Optional[int] = field(default=None)

    @property
    def charge(self) -> int:
        return self.atnum - self.nelec

    @spinpol.setter
    def spinpol(self, value: int) -> None:
        if value not in (1, -1):
            raise ValueError("Spin polarization must be +1 or -1.")
        self.spinpol = value

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, dataset: str, data: Dict[str, Any]) -> 'Species':
        return cls(dataset=dataset, **data)

# Sharded database handler
class SpeciesDB:
    def __init__(self, datapath: str = "atomdb_data"):
        self.datapath = datapath
        os.makedirs(self.datapath, exist_ok=True)
        self.dbs: Dict[str, TinyDB] = {}  # Cache of open TinyDB instances

    def _get_db(self, elem: str) -> TinyDB:
        """Get or create a TinyDB instance for a specific element."""
        if elem not in self.dbs:
            db_path = f"{self.datapath}/{elem}_species.zip"
            self.dbs[elem] = TinyDB(db_path, storage=ZipFileStorage)
        return self.dbs[elem]

    def dump(self, species: Species) -> None:
        """Insert a species into the appropriate shard."""
        db = self._get_db(species.elem)
        species.doc_id = db.insert(species.to_dict())
        logger.info(f"Inserted species into shard for {species.elem}: {species}")

    def load(self, elem: str, mult: int, nexc: int = 0, dataset: str = "default") -> Species:
        """Load a species from the appropriate shard."""
        db = self._get_db(elem)
        query = Query()
        result = db.search(
            (query.elem == elem) &
            (query.mult == mult) &
            (query.nexc == nexc) &
            (query.dataset == dataset)
        )
        if result:
            return Species.from_dict(dataset, result[0])
        raise ValueError(f"Species with elem={elem}, mult={mult}, nexc={nexc} not found in shard.")

    def close(self):
        """Close all open TinyDB instances."""
        for db in self.dbs.values():
            db.close()
        self.dbs.clear()

# Example usage
if __name__ == "__main__":
    fields = {
        "elem": "H",
        "atnum": 1,
        "nelec": 1,
        "nspin": 0,
        "nexc": 0,
        "energy": -0.5,
        "mult": 2,
    }

    species = Species(dataset="default", **fields)
    db_handler = SpeciesDB()
    db_handler.dump(species)
    loaded_species = db_handler.load("H", 2, 0)
    logger.info(f"Loaded species: {loaded_species}")
    db_handler.close()