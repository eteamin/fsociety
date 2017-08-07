# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime, timedelta
import aiohttp

REQUESTS = 100
URL = ''


async def get_async():
   async with aiohttp.ClientSession() as session:
    async with session.get(URL) as resp:
        return resp.status


async def main():

    captured_time = datetime.now()
    result = await asyncio.gather(*[asyncio.Task(get_async()) for u in range(1, REQUESTS)], return_exceptions=True)

    total_time = (datetime.now() - captured_time)
    print("Total requests: {} in {}".format(REQUESTS, total_time))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
