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
        # path to the zip file in the "data" folder
        db_path = f"{self.datapath}/{elem}_species.zip"

        # check if the zip file exists in the folder
        if os.path.exists(db_path):
            db = TinyDB(db_path, storage=self.zip_file_storage_class)
            Species = Query()

            result = db.search(
                (Species.elem == elem) &
                (Species.mult == mult) &
                (Species.nexc == nexc) &
                (Species.dataset == dataset)
            )
            db.close()


            if result:
                print(f"data found {result}")
                return self.species_class.from_dict(dataset, result[0])
            else:
                print(f"No matched parameters for {elem} element")
                # raise ValueError("Not found in the database")
        else:
            print(f"{elem} element does not exist in the database")
            # raise ValueError("Does not exist in the database")
        return None  # Return None if nothing is found


    def close(self):
        for db in self.db.values():
            db.close()