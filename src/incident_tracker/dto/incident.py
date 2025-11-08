from dataclasses import dataclass
from datetime import datetime


@dataclass
class IncidentDTO:
    id: str
    status: str
    source: str
    description: str
    created_at: datetime
