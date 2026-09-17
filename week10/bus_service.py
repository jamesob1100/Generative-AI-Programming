"""Bus service model matching the services table."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BusService:
    id: Optional[int]
    name: str