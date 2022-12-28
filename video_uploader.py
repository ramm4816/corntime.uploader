import os
from random import choice
from utils import TerminalColors, MetaData

class VideoUploader:

    def __init__(self, file_path, client_socket_io, client_pyrogram, task, chat_id) -> None:
        self.file_path = file_path
        self.last_upload_progress = 0
        self.client_socket_io = client_socket_io
        self.task = task
        self.chat_id = chat_id
        self.client_pyrogram = client_pyrogram
        self.myhost = os.uname()[1]
        self.file_meta_data = MetaData.get(self.file_path)

    def upload_progress(self, uploaded, total):
        upload_progress = round(uploaded / total * 100)
        if upload_progress - self.last_upload_progress > 4:
            self.last_upload_progress = upload_progress
            self.client_socket_io.emit('update', {
                'type': 'upload_progress',
                'task_id': self.task['_id'],
                'progress': upload_progress,
                'host': self.myhost
            })
            print(TerminalColors.WARNING + f'[{self.task["_id"]}] upload_progress: {upload_progress}' + TerminalColors.ENDC)

    def upload(self):

        self.last_upload_progress = 0

        fields = {
            'video': self.file_path,
            'chat_id': self.chat_id,
            'duration': int(float(self.file_meta_data['duration'])),
            'height': int(self.file_meta_data['coded_height']),
            'width': int(self.file_meta_data['coded_width']),
            'caption': self.task['film_id'],
            'supports_streaming': 'true',
            'progress': self.upload_progress
        }

        with self.client_pyrogram:
            res = self.client_pyrogram.send_video(**fields)

        os.remove(self.file_path)

        return res
