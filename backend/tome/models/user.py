from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class User:
    id: UUID
    name: str
    email: str
    password: str
    two_factor_recovery: Optional[str]
    two_factor_secret: Optional[str]
