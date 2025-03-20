import json
import os
from tinydb import TinyDB
from classes.Species import Species
from classes.ZipFileStorage import ZipFileStorage
from classes.SpeciesDB import SpeciesDB



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


