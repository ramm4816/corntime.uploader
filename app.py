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
import traceback, json, requests

from subprocess import PIPE

class Worker:

    def __init__(self):
        self.api_id = 20886214
        self.api_hash = "ba51cbd8e8f1dd0fce0d755ce0970600"
        self.chat_ids = []
        self.my_host_name = os.uname()[1]

        result = subprocess.run('ffmpeg -version'.split(), stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self.ffmpeg_version = result.stdout


    def run(self, _session):

        while True:

            try:

                session = _session.split('.')[0]

                self.client_pyrogram = Client(session, self.api_id, self.api_hash)
                self.my_host_name = os.uname()[1]


                while True:

                    try:
                        
                        time_start = time.time()

                        task = MasterApi.get_task(self.my_host_name)
                        self.chat_ids = task['chat_ids']

                        task = task['task']

                        downloader = VideoDownloader(task['url'], task)

                        try:
                            download_res = downloader.download()
                            
                            old_meta = download_res['meta_before_combine']
                            downloaded_file_path = download_res['path']

                        except FilmNotFound as e:
                            print(traceback.format_exc())
                            MasterApi.delete_source(task['_id'])
                            continue

                        if downloaded_file_path == False:
                            # SEND INFO TO SERVER WITH ERROR !
                            continue

                        combined_res = VideoCombiner.combine(task, downloaded_file_path)

                        if combined_res == False:
                            # SEND INFO TO SERVER WITH ERROR !
                            continue

                        
                        new_meta = combined_res['meta_after_combine']
                        combined_file_path = combined_res['path']

                        uploader = VideoUploader(combined_file_path, self.client_pyrogram, task, int(random.choice(self.chat_ids)), time_start)
                        upload_response = uploader.upload()

                        if upload_response.id is not None:
                            full_meta = json.dumps({
                                'before_meta': old_meta,
                                'after_meta': new_meta,
                                'ffmpeg': self.ffmpeg_version,
                                'path': combined_file_path
                            })
                            MasterApi.update_task(message_id=upload_response.id, channel_id=upload_response.chat.id, task_id=task['_id'], host=self.my_host_name, full_info=full_meta)

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
            print(f)
            #os.remove(f)

    def check_restart_command(self):
        self.my_host_name = os.uname()[1]

        with open('/home/dev/corntime.uploader/current.version', 'r') as f:
            ver = f.read()
            requests.get(f"https://api.telegram.org/bot6213721919:AAFKhp_8xVPguHsEfUkAdfars903EDzv7d0/sendMessage?chat_id=-1001865394041&text={self.my_host_name} started, version {ver}")



        while True:
            try:
                time.sleep(15)
                is_restart = MasterApi.check_restart(self.my_host_name)
                if is_restart == True:

                    files = glob.glob('files/*')
                    for f in files:
                        print(f)
                        os.remove(f)

                    command = f"sudo service uploader restart".split()
                    subprocess.run(command)
            except Exception as e:
                print(e)
            

    def restart_service(self):

        time.sleep(5400)
        command = f"sudo service uploader restart".split()
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

            processes.append(Process(target=self.restart_service, args=()))
            processes.append(Process(target=self.check_restart_command, args=()))

            for p in processes:
                p.start()
            for p in processes:
                p.join()
            
            time.sleep(100)

if __name__ == '__main__':
    freeze_support()
    uploader = Uploader()
    uploader.run()