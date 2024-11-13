import asyncio
from data.config import API_KEY, MATCH_LINK
from runner import Runner


async def main():
    api_key = API_KEY
    match_id = MATCH_LINK.split("/")[6]
    runner = Runner(api_key=api_key, match_id=match_id)
    await runner.run()


if __name__ == "__main__":
    asyncio.run(main())
