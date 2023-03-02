import os, sys, time
from utils import TerminalColors, MetaData

class VideoUploader:

    def __init__(self, file_path, client_pyrogram, task, chat_id, time_start) -> None:
        self.file_path = file_path
        self.last_upload_progress = 0
        self.task = task
        self.chat_id = chat_id
        self.client_pyrogram = client_pyrogram
        self.myhost = os.uname()[1]
        self.time_start = time_start
        self.file_meta_data = MetaData.get(self.file_path)

    def upload_progress(self, uploaded, total):

        if hasattr(self, "anim_bar_index") == False:
           self.anim_bar_index = 0
           self.anim_bar_symbols = ["-","\\","|","/"]

        upload_progress = round(uploaded / total * 100)

        if upload_progress - self.last_upload_progress > 1:
            self.last_upload_progress = upload_progress

            print(TerminalColors.WARNING + f'[{self.task["_id"]}] upload_progress: {upload_progress}' + TerminalColors.ENDC)

    def upload(self):

        self.last_upload_progress = 0

        executed_time = round(time.time() - self.time_start)

        caption = f"Film_id: {self.task['film_id']}\n\Executed time: {executed_time}\nHost: {self.myhost}"
        
        fields = {
            'video': self.file_path,
            'chat_id': self.chat_id,
            'duration': int(float(self.file_meta_data['duration'])),
            'height': int(self.file_meta_data['coded_height']),
            'width': int(self.file_meta_data['coded_width']),
            'caption': caption,
            'supports_streaming': 'true',
            'progress': self.upload_progress
        }

        with self.client_pyrogram:
            res = self.client_pyrogram.send_video(**fields)

        #os.remove(self.file_path)




        return res
