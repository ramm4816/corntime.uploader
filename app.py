import os, traceback, time, os, requests, socketio, time, glob, random
from multiprocessing import Process
from pyrogram import Client
from utils import TerminalColors
from master_api import MasterApi
from multiprocessing import freeze_support

from video_downloader import VideoDownloader
from video_combiner import VideoCombiner
from video_uploader import VideoUploader

class Worker:

    def __init__(self):
        self.api_id = 20886214
        self.api_hash = "ba51cbd8e8f1dd0fce0d755ce0970600"
        self.chat_ids = []


    def run(self, session):

        self.client_pyrogram = Client(session, self.api_id, self.api_hash)
        self.client_socket_io = socketio.Client()
        self.my_host_name = os.uname()[1]

        self.client_socket_io.connect('https://fykp.ru/socket.io')

        print(TerminalColors.OKGREEN + f'Connected to socket io, my session_id: {self.client_socket_io.sid}\n' + TerminalColors.ENDC)

        while True:

            try:
                
                task = MasterApi.get_task()
                self.chat_ids = task['chat_ids']

                #self.client_pyrogram.start()
                #for link in res['links']:
                #    self.client_pyrogram.join_chat(link)
                #    sleep(60)

                task = task['task']

                self.client_socket_io.emit('update', {'type': 'show_task', 'task_id': task['_id'], 'host': self.my_host_name})


                downloader = VideoDownloader(task['url'], self.client_socket_io, task)
                downloaded_file_path = downloader.download()

                if downloaded_file_path == False:
                    # SEND INFO TO SERVER WITH ERROR !
                    continue

                combined_file_path = VideoCombiner.combine(self.client_socket_io, task, downloaded_file_path)

                if combined_file_path == False:
                    # SEND INFO TO SERVER WITH ERROR !
                    continue

                uploader = VideoUploader(combined_file_path, self.client_socket_io, self.client_pyrogram, task, int(random.choice(self.chat_ids)))
                upload_response = uploader.upload()

                if upload_response.id is not None:
                    MasterApi.update_task(message_id=upload_response.id, channel_id=upload_response.chat.id, task_id=task['_id'], host=self.my_host_name)
                    self.client_socket_io.emit('update', {'type': 'upload_success', 'task_id': task['_id'], 'host': self.my_host_name})

            except Exception as e:
                #print(e)
                traceback.print_exc()
                time.sleep(300)

            time.sleep(1)
            

class Uploader:

    def remove_files_before_run(self):
        files = glob.glob('files/*')
        for f in files:
            os.remove(f)

    def run(self):

        self.remove_files_before_run()

        while True:
            processes = []
            sessions = glob.glob('*.session')
            for session in sessions:
                print(session)
                worker = Worker()
                processes.append(Process(target=worker.run, args=(session,)))
            for p in processes:
                p.start()
            for p in processes:
                p.join()
            
            time.sleep(100)
if __name__ == '__main__':
    freeze_support()
    uploader = Uploader()
    uploader.run()


