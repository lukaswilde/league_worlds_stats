import json
from enum import Enum
from pydantic import BaseModel, NonNegativeInt, conlist, HttpUrl, PositiveInt, \
    constr, Field
from typing import Optional, Literal
from datetime import datetime

class EventState(Enum):
    completed = "completed"
    unstarted = "unstarted"

class Outcome(Enum):
    loss = "loss"
    win = "win"

class Pages(BaseModel):
    older: Optional[str]
    newer: Optional[str]

class League(BaseModel):
    name: str   # here: "WM"
    slug: str   # here: "worlds"

class Result(BaseModel):
    outcome: Optional[Outcome]
    gameWins: NonNegativeInt

class Record(BaseModel):
    wins: NonNegativeInt
    losses: NonNegativeInt

class Team(BaseModel):
    name: str
    code: str
    image: HttpUrl
    result: Optional[Result]
    record: Optional[Record]

class Strategy(BaseModel):
    type: str   # here: "bestOf"
    count: PositiveInt

class Match(BaseModel):
    id: NonNegativeInt
    flags: list[str]
    teams: conlist(Team, min_length=2, max_length=2)
    strategy: Strategy

class Event(BaseModel):
    startTime: datetime
    state: EventState
    type: Literal["match"]
    blockName: str
    league: League
    match: Match

class Schedule(BaseModel):
    pages: Pages
    events: list[Event]
