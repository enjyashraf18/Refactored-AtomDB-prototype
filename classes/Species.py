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


    def __post_init__(self):
        # customization for dataset only (temp)
        self.dataset = self.dataset.lower()

    def to_dict(self):
        return asdict(self)

    def get_data(self):
        return self.to_dict()

    @classmethod
    def from_dict(cls, dataset: str, data):
        return cls(**data)

    @property
    def charge(self):
        return self.atnum - self.nelec