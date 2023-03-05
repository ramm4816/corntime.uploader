import os, sys, time
from utils import TerminalColors, MetaData

from telethon.sync import TelegramClient, events
from telethon.tl.types import DocumentAttributeVideo 
from utils import TerminalColors, MetaData
from telethon.tl.custom.file import File
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from pyrogram import Client

class VideoUploader:

    def __init__(self, file_path, session, task, chat_id, time_start) -> None:
        self.file_path = file_path
        self.last_upload_progress = 0
        self.task = task
        self.chat_id = chat_id
        self.api_id = 20886214
        self.api_hash = "ba51cbd8e8f1dd0fce0d755ce0970600"
        self.session = session
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
        


        if 'telethon' not in self.session:
            self.telegram_client = Client(self.session, self.api_id, self.api_hash)
            self.telegram_client_type = 'pyrogram'
        else:
            self.telegram_client = TelegramClient(self.session, self.api_id, self.api_hash)
            self.telegram_client_type = 'telethon'


        if self.telegram_client_type == 'pyrogram':

            with self.telegram_client:
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

                res = self.telegram_client.send_video(**fields)

                return {
                    'id': res.id,
                    'channel_id': res.chat.id
                }
        
        else:
            with self.telegram_client:
                file = self.telegram_client.upload_file(self.file_path, progress_callback=self.upload_progress)
                res = self.telegram_client.send_file(int( self.chat_id), file, attributes=(DocumentAttributeVideo(duration=int(float(self.file_meta_data['duration'])), w=int(self.file_meta_data['coded_width']), h=int(self.file_meta_data['coded_height']), supports_streaming=True),))

                return {
                    'id': res.id,
                    'channel_id': '-100'+str(res.peer_id.channel_id)
                }
        #os.remove(self.file_path)

