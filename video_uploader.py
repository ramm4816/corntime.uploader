import os, sys, time
from utils import TerminalColors, MetaData

class VideoUploader:

    def __init__(self, file_path, client_socket_io, client_pyrogram, task, chat_id, time_start) -> None:
        self.file_path = file_path
        self.last_upload_progress = 0
        self.client_socket_io = client_socket_io
        self.task = task
        self.chat_id = chat_id
        self.client_pyrogram = client_pyrogram
        self.myhost = os.uname()[1]
        self.time_start = time_start
        print(file_path)
        self.file_meta_data = MetaData.get(self.file_path)

    def upload_progress(self, uploaded, total):

        if hasattr(self, "anim_bar_index") == False:
           self.anim_bar_index = 0
           self.anim_bar_symbols = ["-","\\","|","/"]

        upload_progress = round(uploaded / total * 100)

        if upload_progress - self.last_upload_progress > 1:
            self.last_upload_progress = upload_progress
            self.client_socket_io.emit('update', {
                'type': 'upload_progress',
                'task_id': self.task['_id'],
                'progress': upload_progress,
                'host': self.myhost
            })
            
            print(TerminalColors.WARNING + f'[{self.task["_id"]}] upload_progress: {upload_progress}' + TerminalColors.ENDC)

            '''
            size = 50
            x = round(upload_progress / 100 * size)

            prefix = f"Uploading: {self.anim_bar_symbols[self.anim_bar_index]} "
            self.anim_bar_index += 1
            if self.anim_bar_index > 3:
                self.anim_bar_index = 0
            
            print(TerminalColors.WARNING + "{}{}{} {}/{}".format(prefix, u'█'*x, "░"*(size-x), upload_progress, 100) + TerminalColors.ENDC, end='\r', file=sys.stdout, flush=True)

            '''

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

        os.remove(self.file_path)

        return res
