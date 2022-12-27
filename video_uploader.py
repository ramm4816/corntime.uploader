import os
from random import choice
from utils import TerminalColors

class video_uploader:

    def __init__(self, file_path, sio, task) -> None:
        self.file_path = file_path
        self.last_upload_progress = 0
        self.sio = sio
        self.task = task
        self.myhost = os.uname()[1]

    def upload_progress(self, uploaded, total):
        upload_progress = round(uploaded / total * 100)
        if upload_progress - self.last_upload_progress > 4:
            self.last_upload_progress = upload_progress
            self.sio.emit('update', {
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
            'chat_id': int(choice(self.chat_ids)),
            'duration': int(float(data['meta']['duration'])),
            'height': int(data['meta']['coded_height']),
            'width': int(data['meta']['coded_width']),
            'caption': self.task['film_id'],
            'supports_streaming': 'true',
            'progress': self.upload_progress
        }

        with self.pycl:
            res = self.pycl.send_video(**fields)
            print(res)

        os.remove(data['filename'])

        return {
            'res': res
        }
