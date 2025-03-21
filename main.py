import json
import os
from classes.Species import Species
from classes.SpeciesDB import SpeciesDB
from classes.ZipFileStorage import ZipFileStorage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    fields = {
        "elem": "X",
        "atnum": 1,
        "nelec": 1,
        "nspin": 0,
        "nexc": 0,
        "energy": -0.35,
        "mult": 3,
    }

    # initialization
    species_db = SpeciesDB("data", {}, Species, ZipFileStorage)
    species = Species(dataset="default", fields=fields)

    # dump species to db
    species_db.dump(species)

    species_db.close()

    # found in the db
    loaded_species = species_db.load("X", 3, 0)

    # element found in the db but with different parameters
    loaded_species = species_db.load("X", 2, 0)

    #not found in the db
    loaded_species = species_db.load("Q", 3, 0)

    # logger.info(f"Loaded species: {loaded_species}")




