"""Bus model matching the buses table."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Bus:
    id: Optional[int]
    service_id: int
    bus_model_id: int
    schedule_type: str
    weekend: bool
    workday: bool