"""Bus model matching the bus_models table."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BusModel:
    id: Optional[int]
    name: str
    seats: int