import wget, os, uuid, sys
from utils import TerminalColors, MetaData
from pathlib import Path
from exceptions import FilmNotFound


class VideoDownloader:

    def __init__(self, url, task):
        
        self.root_dir = Path().absolute()
        self.url = url
        self.last_download_progress = 0
        self.task = task
        self.myhost = os.uname()[1]
        self.unique_filename = str(uuid.uuid4()) + '.mp4'
        self.file_path = f'{self.root_dir}/files/{self.unique_filename}'


    def download_progress(self, total_downloaded, total_length, width = 100):

        if hasattr(self, "anim_bar_index") == False:
           self.anim_bar_index = 0
           self.anim_bar_symbols = ["-","\\","|","/"]

        download_progress = round(total_downloaded / total_length * 100)

        if download_progress - self.last_download_progress >= 1:
            self.last_download_progress = download_progress

            print(TerminalColors.WARNING + f'[{self.task["_id"]}] download_progress: {download_progress}' + TerminalColors.ENDC)
        
    def download(self):

        try:
            wget.download(self.url, self.file_path, bar=self.download_progress)
        except Exception as e:
            raise FilmNotFound


        meta = MetaData.get(self.file_path)

        if float(meta['duration']) < 1000:
            print(
                TerminalColors.FAIL + f'[{self.task["_id"]}] duration < 1000, return false' + TerminalColors.ENDC)
            raise FilmNotFound

        return self.file_path