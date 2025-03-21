from tinydb import TinyDB, Query
import os
from typing import Optional

class SpeciesDB:
    """Handles database operations for Species"""

    def __init__(self, datapath: str, db: dict, species_class, zip_file_storage_class):
        self.datapath = datapath
        self.db = db
        self.species_class = species_class

        # storing the class itself, not an instance
        self.zip_file_storage_class = zip_file_storage_class

        os.makedirs(self.datapath, exist_ok=True)

    def get_db(self, elem):
        if elem not in self.db:
            self.create_db(elem)
        print(f"db[elem] in get_db {self.db[elem]}")
        return self.db[elem]

    def get_db2(self, elem):
        if elem not in self.db:
            return None
        return self.db[elem]

    def create_db(self, elem: str):
        db_path = f"{self.datapath}/{elem}_species.zip"
        self.db[elem] = TinyDB(db_path, storage=self.zip_file_storage_class)

    def dump(self, species):
        db = self.get_db(species.elem)
        Species = Query()
        # check if species already exists
        existing = db.search(
            (Species.elem == species.elem) &
            (Species.mult == species.mult) &
            (Species.nexc == species.nexc) &
            (Species.dataset == species.dataset)
        )
        if not existing:
            db.insert(species.to_dict())


    def load(self, elem: str, mult, nexc=0, dataset: str = "default"):
        db = self.get_db2(elem)
        if db is not None:
            Species = Query()
            result = db.search(
                (Species.elem == elem) &
                (Species.mult == mult) &
                (Species.nexc == nexc) &
                (Species.dataset == dataset)
            )
            if result:
                print(f"data found {result}")
                return self.species_class.from_dict(dataset, result[0])
            else:
                raise ValueError("Not found in the database")

        else:
            raise ValueError("Does not exist in the database")


    def close(self):
        for db in self.db.values():
            db.close()