import json
import httpx
from datetime import datetime
from models.event_details import EventDetails
from models.game_details import GameDetails
from models.schedule import Schedule

API_KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
WORLDS_ID = 98767975604431411   # for world championship

class LeagueRequestHandler():
    _api_key: str
    _league_id: int
    def __init__(self, api_key: str, league_id: int):
        self._api_key = api_key
        self._league_id = league_id

    def _get_esports_endpoint(self, endpoint: str, url_params: dict[str, str | int]) -> json:
        url = f"https://esports-api.lolesports.com/persisted/gw/{endpoint}"
        headers = {"x-api-key": self._api_key}
        params = {"hl": "en-US"} | url_params
        response = httpx.get(url, headers=headers, params=params)
        return response.json()

    def get_schedule(self) -> json:
        schedule = self._get_esports_endpoint("getSchedule", url_params={"leagueId": self._league_id})
        schedule = schedule["data"]["schedule"]
        return Schedule(**schedule)

    def get_event_details(self, match_id: int) -> EventDetails:
        event = self._get_esports_endpoint("getEventDetails", url_params={"id": match_id})
        event = event["data"]["event"]
        return EventDetails(**event)

    def get_window(self, game_id: int, starting_time: datetime = None) -> GameDetails:
        url = f"https://feed.lolesports.com/livestats/v1/window/{game_id}"
        params = dict()
        params["startingTime"] =  starting_time
        response = httpx.get(url, params=params)
        window = response.json()
        return GameDetails(**window)

    def get_game_start(self, game_id: int) -> datetime:
        window = self.get_window(game_id)
        return window.frames[0].rfc460Timestamp
