import wget
import os
import uuid
from utils import TerminalColors, MetaData


class VideoDownloader:

    def __init__(self, url, sio, task):

        self.url = url
        self.last_download_progress = 0
        self.sio = sio
        self.task = task
        self.myhost = os.uname()[1]
        self.unique_filename = str(uuid.uuid4()) + '.mp4'
        self.file_path = f'files/{self.unique_filename}'

    def download_progress(self, total_downloaded, total_length, width=80):
        download_progress = round(total_downloaded / total_length * 100)
        if download_progress - self.last_download_progress > 4:
            self.last_download_progress = download_progress
            self.sio.emit('update', {
                'type': 'download_progress',
                'task_id': self.task['_id'],
                'progress': download_progress,
                'host': self.myhost
            })
            print(TerminalColors.WARNING + f'[{self.task["_id"]}] download_progress: {download_progress}' + TerminalColors.ENDC)

    def download(self, url):
        wget.download(url, self.file_path, bar=self.download_progress)
        meta = MetaData.get(self.file_path)

        if float(meta['duration']) < 1000:
            print(
                TerminalColors.FAIL + f'[{self.task["_id"]}] duration < 1000, return false' + TerminalColors.ENDC)
            return False

        return self.file_path