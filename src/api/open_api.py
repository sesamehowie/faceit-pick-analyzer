from src.client.client import Client
from src.utils.decorators import retry


class OpenApi(Client):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)
        self.api_key = api_key
        self.base_url = "https://open.faceit.com/data/v4"

    @retry
    async def get_match_details(self, match_id: str) -> dict:
        """Function: get_match_details(match_id: string)"""
        response = await self.session_request(
            method="GET",
            url=self.base_url + f"/matches/{match_id}",
            headers=self.headers,
        )
        return response

    @retry
    async def get_player_stats(self, player_id: str) -> dict:
        """Function: get_player_stats(player_id: string)"""
        response = await self.session_request(
            method="GET",
            url=self.base_url + f"/players/{player_id}/stats/cs2",
            headers=self.headers,
        )
        return response
