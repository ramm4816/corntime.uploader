 
from pyrogram import Client
import os, traceback, time, os, time, glob, random, subprocess
import asyncio
import shutil
from utils import TerminalColors, MetaData





api_id = 20886214
api_hash = "ba51cbd8e8f1dd0fce0d755ce0970600"
file_path = 't1.mp4'

file_meta_data = MetaData.get(file_path)

def upload_progress(uploaded, total):
   print(round(uploaded/total*100))


async def main():
    async with Client('myaccpyro', api_id, api_hash) as app:

      fields = {
         'video': file_path,
         'chat_id': 804897324,
         'duration': int(float(file_meta_data['duration'])),
         'height': int(file_meta_data['coded_height']),
         'width': int(file_meta_data['coded_width']),
         'caption': 'ПИРОГ ЁБАНЫЙ',
         'supports_streaming': 'true',
         'progress': upload_progress
      }

      res = await app.send_video(**fields)

asyncio.run(main())




         