from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional

@dataclass
class Species:
    """
    Species is a class for representing atomic and ionic species.
    """

    def __init__(self, dataset, fields, spinpol=1, doc_id=None):
        super().__init__(value=fields, doc_id=doc_id)
        self._dataset = dataset.lower()
        self._spinpol = spinpol
        self._fields = fields

        # Instead of manually assigning each field (for ex: self.elem = fields["elem"])
        for field_name, value in fields.items():
            setattr(self, field_name, value)

    def to_dict(self):
        # if no Conversion Required anymore
        # return self._fields
        return asdict(self._fields)



    def get_data(self):
        """simply returns self._fields dict"""
        return self._fields

    @classmethod
    def from_dict(cls, dataset, data):
        """create a species instance from a dictionary"""
        return cls(dataset, data)


    @property
    def dataset(self):
        """return the dataset name"""
        return self._dataset

    @property
    def charge(self):
        return self._fields.atnum - self._fields.nelec