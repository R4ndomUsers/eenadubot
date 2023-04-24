from aiohttp import ClientSession, ClientTimeout
from asyncio import sleep
from os import environ


async def ping_server():
    if BASE_URL:= environ.get['RENDER_EXTERNAL_URL']:
        while True:
            try:
                async with ClientSession(timeout=ClientTimeout(total=10)) as session:
                    async with session.get(BASE_URL) as _:
                        pass
                await sleep(600)
            except Exception as e:
                print(e)
                await sleep(25)
                continue