from dataclasses import dataclass
from datetime import datetime


@dataclass
class ServiceDTO:
    id: str
    name: str
    created_at: datetime
    scopes: list[str]


@dataclass
class NewServiceDTO:
    name: str
    scopes: list[str]
