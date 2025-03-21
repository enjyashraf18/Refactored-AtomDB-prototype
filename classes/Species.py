from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class Species:
    """
    Species is for representing atomic and ionic species
    """

    dataset: str
    elem: str
    atnum: int
    nelec: int
    nspin: int
    nexc: int
    energy: float
    mult: int
    spinpol: int = 1
    doc_id: int = None

    def __init__(self, dataset: str, fields, spinpol= 1, doc_id: int = None):
        self.dataset = dataset.lower()
        self.spinpol = spinpol
        self.doc_id = doc_id

        # Instead of manually assigning each field (for ex: self.elem = fields["elem"])
        for field_name, value in fields.items():
            setattr(self, field_name, value)

    def to_dict(self):
        return asdict(self)

    def get_data(self):
        return self.to_dict()

    @classmethod
    def from_dict(cls, dataset: str, data):
        return cls(dataset, data)

    @property
    def charge(self):
        return self.atnum - self.nelec