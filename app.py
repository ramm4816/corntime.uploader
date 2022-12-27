import os, asyncio, pymongo, traceback, sys, random
from multiprocessing import Process, Pool, Queue, Manager
import time, random, sys, os
from dotenv import load_dotenv
from time import time, sleep
import uuid, requests
import ffmpeg
from pprint import pprint
import subprocess
from random import choice
load_dotenv()
import urllib.request
from pyrogram import Client, filters
from pget.down import Downloader
import socketio
import time
import glob
import moviepy
import moviepy.editor as mp
from os.path import exists
from utils import TerminalColors


ROOT_PATH = '/home/dev/uploader'



INTROS = [
    {'file':'/home/dev/uploader/intros/m1.mp4',  'name':'m1'},
    {'file':'/home/dev/uploader/intros/m2.mp4',  'name':'m2'},
    {'file':'/home/dev/uploader/intros/m3.mp4',  'name':'m3'},
    {'file':'/home/dev/uploader/intros/f1.mp4',  'name':'f1'},
    {'file':'/home/dev/uploader/intros/f2.mp4',  'name':'f2'},
    {'file':'/home/dev/uploader/intros/f3.mp4',  'name':'f3'},
    {'file':'/home/dev/uploader/intros/f21.mp4',  'name':'f21'},
    {'file':'/home/dev/uploader/intros/f22.mp4',  'name':'f22'},
    {'file':'/home/dev/uploader/intros/f23.mp4',  'name':'f23'},
]

class Worker:

    def __init__(self):
        self.api_id = 20886214
        self.api_hash = "ba51cbd8e8f1dd0fce0d755ce0970600"
        self.chat_ids = []


    def run(self, session_num):

        self.pycl = Client(f"s{session_num}", self.api_id, self.api_hash)
        self.sio = socketio.Client()
        self.myhost = os.uname()[1]

        self.sio.connect('https://fykp.ru/socket.io')

        print(TerminalColors.OKBLUE + f'Connected to socket io, my session_id: {self.sio.sid}' + TerminalColors.ENDC)

        while True:
            try:
                
                print(res)
                self.chat_ids = res['chat_ids']

            
                '''
                self.pycl.start()
                for link in res['links']:
                    self.pycl.join_chat(link)
                    sleep(60)
                '''


                self.task = res['task']

                self.sio.emit('update', {
                    'type': 'add_task',
                    'task_id': self.task['_id'],
                    'host': self.myhost
                })

                print(f'download: {self.task["url"]}')
                
                data = self.download_file(self.task['url'])

                if data == False:
                    continue

                res = self.upload_file(data)

                if res['res'].id is not None:
                    requests.post("https://fykp.ru/api/update_tasks", data={
                        'message_id': res['res'].id,
                        'channel_id': res['res'].chat.id,
                        'task_id': self.task['_id'],
                        'host': self.myhost
                    })
                    self.sio.emit('update', {
                        'type': 'upload_success',
                        'task_id': self.task['_id'],
                        'host': self.myhost
                    })

            
            except Exception as e:
                #print(e)
                traceback.print_exc()
            time.sleep(1)

async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")

class Uploader:

    def remove_files_before_run(self):
        files = glob.glob('files/*')
        for f in files:
            os.remove(f)

    def run(self):

        self.remove_files_before_run()

        while True:
            processes = []
            for i in [10]:
                worker = Worker()
                processes.append(Process(target=worker.run, args=(i,)))
            for p in processes:
                p.start()
            for p in processes:
                p.join()


uploader = Uploader()
uploader.run()


