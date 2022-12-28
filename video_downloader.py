import wget, os, uuid, sys
from utils import TerminalColors, MetaData

class VideoDownloader:

    def __init__(self, url, client_socket_io, task):

        self.url = url
        self.last_download_progress = 0
        self.client_socket_io = client_socket_io
        self.task = task
        self.myhost = os.uname()[1]
        self.unique_filename = str(uuid.uuid4()) + '.mp4'
        self.file_path = f'files/{self.unique_filename}'


 


    def download_progress(self, total_downloaded, total_length, width = 100):
        download_progress = round(total_downloaded / total_length * 100)
        if download_progress - self.last_download_progress > 4:
            self.last_download_progress = download_progress
            self.client_socket_io.emit('update', {
                'type': 'download_progress',
                'task_id': self.task['_id'],
                'progress': download_progress,
                'host': self.myhost
            })

            size = 50
            x = round(download_progress / width * size)
            prefix = "Downloading: "
            
            print(TerminalColors.WARNING + "{}{}{} {}/{}".format(prefix, u'█'*x, "░"*(size-x), download_progress, width) + TerminalColors.ENDC, end='\r', file=sys.stdout, flush=True)


    def download(self):

        wget.download(self.url, self.file_path, bar=self.download_progress)

        meta = MetaData.get(self.file_path)

        if float(meta['duration']) < 1000:
            print(
                TerminalColors.FAIL + f'[{self.task["_id"]}] duration < 1000, return false' + TerminalColors.ENDC)
            return False

        return self.file_path