from classes.ZipFileStorage import ZipFileStorage




import json
import os
from classes.Species import Species
from classes.SpeciesDB import SpeciesDB
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


