"""Run model matching the runs table."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Run:
    id: Optional[int]
    service_id: int
    run_date: str