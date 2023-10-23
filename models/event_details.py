from enum import Enum
from pydantic import BaseModel, NonNegativeInt, conlist, HttpUrl, PositiveInt
from typing import Optional, Literal
from datetime import datetime

class Tournament(BaseModel):
    id: NonNegativeInt

class League(BaseModel):
    id: NonNegativeInt
    slug: str   # here: "worlds"
    image: HttpUrl
    name: str   # here: "WM"

class Strategy(BaseModel):
    count: NonNegativeInt

class Result(BaseModel):
    gameWins: NonNegativeInt

class Team(BaseModel):
    id: NonNegativeInt
    name: str
    code: str
    image: HttpUrl
    result: Optional[Result]

class GameState(Enum):
    completed = "completed"
    unneeded = "unneeded"
    unstarted = "unstarted"

class Side(Enum):
    blue = "blue"
    red = "red"

class ShortTeam(BaseModel):
    id: NonNegativeInt
    side: Optional[Side]

class MediaLocale(BaseModel):
    locale: str
    englishName: str
    translatedName: str

class Vod(BaseModel):
    id: NonNegativeInt
    parameter: str
    locale: str
    mediaLocale: MediaLocale
    provider: str
    offset: NonNegativeInt
    firstFrameTime: datetime
    startMillis: Optional[NonNegativeInt]
    endMillis: Optional[NonNegativeInt]

class Game(BaseModel):
    number: PositiveInt
    id: NonNegativeInt
    state: GameState
    teams: conlist(ShortTeam, min_length=2, max_length=2)
    vods: list[Vod]

class Match(BaseModel):
    strategy: Strategy
    teams: conlist(Team, min_length=2, max_length=2)
    games: list[Game]

class Event(BaseModel):
    id: NonNegativeInt
    type: Literal["match"]
    tournament: Tournament
    league: League
    match: Match