"""Ticket model matching the tickets table."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Ticket:
    id: Optional[int]
    user_id: int
    run_id: int