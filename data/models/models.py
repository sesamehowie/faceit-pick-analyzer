from decimal import Decimal
from pydantic import BaseModel
from enum import Enum


class TeamIdentifier(Enum):
    Enemy = 0
    Ally = 1
    Unset = 2


class Map(BaseModel):
    label: str
    win_rate_percentage: int | float | Decimal


class User(BaseModel):
    id: int | str
    faceit_name: str


class Team(BaseModel):
    name: str
    team_identifier: int
    players: list[User]
