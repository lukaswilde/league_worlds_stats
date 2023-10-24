from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, NonNegativeInt, PositiveInt, conint, conlist


class Role(StrEnum):
    TOP = "top"
    JUNGLE = "jungle"
    MID = "mid"
    BOTTOM = "bottom"
    SUPPORT = "support"


class Participant(BaseModel):
    participantId: PositiveInt
    esportsPlayerId: NonNegativeInt
    summonerName: str
    championId: str
    role: Role


class TeamMetadata(BaseModel):
    esportsTeamId: NonNegativeInt
    participantMetadata: conlist(Participant, min_length=5, max_length=5)


class Metadata(BaseModel):
    patchVersion: str
    blueTeamMetadata: TeamMetadata
    redTeamMetadata: TeamMetadata


class GameState(StrEnum):
    IN_GAME = "in_game"
    FINISHED = "finished"


class Dragon(StrEnum):
    INFERNAL = "infernal"
    HEXTECH = "hextech"
    MOUNTAIN = "mountain"
    CLOUD = "cloud"
    OCEAN = "ocean"
    CHEMTECH = "chemtech"


class ParticipantStats(BaseModel):
    participantId: NonNegativeInt
    totalGold: NonNegativeInt
    level: conint(ge=1, le=18)
    kills: NonNegativeInt
    deaths: NonNegativeInt
    assists: NonNegativeInt
    creepScore: NonNegativeInt
    currentHealth: NonNegativeInt
    maxHealth: NonNegativeInt


class TeamStats(BaseModel):
    totalGold: NonNegativeInt
    inhibitors: conint(ge=0, le=3)
    towers: conint(ge=0, le=11)
    barons: NonNegativeInt
    totalKills: NonNegativeInt
    dragons: conlist(Dragon, min_length=0, max_length=4)
    participants: conlist(ParticipantStats, min_length=5, max_length=5)


class Frame(BaseModel):
    rfc460Timestamp: datetime
    gameState: GameState
    blueTeam: TeamStats
    redTeam: TeamStats


class GameDetails(BaseModel):
    esportsGameId: NonNegativeInt
    esportsMatchId: NonNegativeInt
    gameMetadata: Metadata
    frames: list[Frame]
