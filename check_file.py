from pyrogram import Client
import os, traceback, time, os, time, glob, random, subprocess
import asyncio
import shutil

sessions = glob.glob('*.session')
     
for session in sessions:
    _session = session
    session = _session.split('.')[0]

api_id = 20886214
api_hash = "ba51cbd8e8f1dd0fce0d755ce0970600"

async def main():
    async with Client(session, api_id, api_hash) as app:

        messages = await app.get_messages(-1001365260888, [40143])

        message = messages[0]
        f = open('checker.mp4','wb')
        async for chunk in app.stream_media(message):
            f.write(chunk)
            print(len(chunk))

asyncio.run(main())
