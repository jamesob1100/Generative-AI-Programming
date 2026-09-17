"""User model matching the users table."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    admin: bool
    username: str
    password: str