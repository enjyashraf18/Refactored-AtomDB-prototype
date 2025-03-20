from tinydb import TinyDB, Query
from tinydb.table import Document
from dataclasses import asdict, fields
import json

class Species(Document):
    """
    Species is a class for representing atomic and ionic species.
    """

    def __init__(self, dataset, fields, spinpol=1, doc_id=None):
        #why kwargs??
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
    print("Database contents:", db.all())  # Debug print
    query = Query()
    result = db.search(
        (query.elem == elem)
        & (query.mult == mult)
        & (query.nexc == nexc)
    )
    print(f"hena result {result}")
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
        "mult": 1,
    }
species = Species("default", fields)
print(f"here is species  {species} ")
dump(species)
loaded_species = load("H", 1, 0)
print(f"here load {loaded_species}")