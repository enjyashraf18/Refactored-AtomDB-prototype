from tinydb import TinyDB
import os


class SpeciesDB:
    """Handles database operations for Species"""

    def __init__(self, datapath, db, species, zip_file_storage):
        self.datapath = datapath
        self.db = db
        self.species = species
        self.zip_file_storage = zip_file_storage

        # creating the folder if it does not exist
        os.makedirs(self.datapath, exist_ok=True)


    def get_db(self, elem):
        # checks if we already have a database for this element
        if elem not in self.db:
            self.create_db(elem)
        return self.db[elem]

    def create_db(self, elem):
        db_path = f"{self.datapath}/{elem}_species.zip"
        self.db[elem] = TinyDB(db_path, storage=self.zip_file_storage)

    def dump(self):
        pass

    def load(self, elem: str, mult: int, nexc: int = 0, dataset: str = "default"):
        pass