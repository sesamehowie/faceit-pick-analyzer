import aiohttp
from typing import Self


class Client:

    def __init__(self, api_key: str) -> Self:
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def session_request(
        self, method: str, url: str, headers: dict | None = None
    ) -> dict | None:

        async with aiohttp.ClientSession() as session:
            session.headers.update(self.headers)
            response = await session.request(method, url)
            data = await response.json()
            return data
