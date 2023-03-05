from telethon.sync import TelegramClient, events
from telethon.tl.types import DocumentAttributeVideo 
from utils import TerminalColors, MetaData
from telethon.tl.custom.file import File


from telethon.tl.types import PeerUser, PeerChat, PeerChannel


path = 'intro/intro.mp4'

file_meta_data = MetaData.get(path)


def handle_progress(progress,total):
   print(round(progress / total * 100))

with TelegramClient('3d3a529f-2765-4acf-80dd-812fdc2f66e7', 20886214, "ba51cbd8e8f1dd0fce0d755ce0970600") as client:
   
   file = client.upload_file('intro/intro.mp4', progress_callback=handle_progress)
   
   res = client.send_file(-1001805877872, file, attributes=(DocumentAttributeVideo(duration=int(float(file_meta_data['duration'])), w=int(file_meta_data['coded_width']), h=int(file_meta_data['coded_height']), supports_streaming=True),), supports_streaming=True)

   print(res)
   print('-100'+str(res.peer_id.channel_id))

   client.run_until_disconnected()


