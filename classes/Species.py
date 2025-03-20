import json
import os
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional



@dataclass
class Species:
    dataset: str
    elem: str
    atnum: int
    nelec: int
    nspin: int
    nexc: int
    energy: float
    mult: int
    spinpol: int = field(default=1)
    doc_id: Optional[int] = field(default=None)

