import os, traceback, time, os, time, glob, random, subprocess
from multiprocessing import Process
from pyrogram import Client
from utils import TerminalColors
from master_api import MasterApi
from multiprocessing import freeze_support

from video_downloader import VideoDownloader
from video_combiner import VideoCombiner
from video_uploader import VideoUploader


from exceptions import FilmNotFound


class Worker:

    def __init__(self):
        self.api_id = 20886214
        self.api_hash = "ba51cbd8e8f1dd0fce0d755ce0970600"
        self.chat_ids = []


    def run(self, _session):

        while True:

            try:

                session = _session.split('.')[0]

                self.client_pyrogram = Client(session, self.api_id, self.api_hash)
                self.my_host_name = os.uname()[1]


                while True:

                    try:
                        
                        time_start = time.time()

                        task = MasterApi.get_task()
                        self.chat_ids = task['chat_ids']

                        task = task['task']

                        downloader = VideoDownloader(task['url'], task)
                        try:
                            downloaded_file_path = downloader.download()
                        except FilmNotFound as e:
                            MasterApi.delete_source(task['_id'])
                            continue

                        if downloaded_file_path == False:
                            # SEND INFO TO SERVER WITH ERROR !
                            continue

                        combined_file_path = VideoCombiner.combine(task, downloaded_file_path)

                        if combined_file_path == False:
                            # SEND INFO TO SERVER WITH ERROR !
                            continue

                        uploader = VideoUploader(combined_file_path, self.client_pyrogram, task, int(random.choice(self.chat_ids)), time_start)
                        upload_response = uploader.upload()

                        if upload_response.id is not None:
                            MasterApi.update_task(message_id=upload_response.id, channel_id=upload_response.chat.id, task_id=task['_id'], host=self.my_host_name)

                    except Exception as e:
                        #print(e)
                        traceback.print_exc()
                        time.sleep(5)

                    time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(1)

class Uploader:

    def remove_files_before_run(self):
        files = glob.glob('files/*')
        for f in files:
            os.remove(f)


    def restart_service(self):

        time.sleep(10)
        command = f"sudo service uploader stop".split()
        subprocess.run(command)
        

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