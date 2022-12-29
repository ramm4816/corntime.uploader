from utils import TerminalColors, MetaData
from pathlib import Path
import uuid, subprocess


meta = MetaData.get('files/3df0fc77-b21f-451e-9c7b-4cadef82c92b.mp4')
print(meta)

meta = MetaData.get('files/df4d535a-a2f8-47da-acf5-25b71b766dd3.mp4')
print(meta)

exit()



root_dir = Path().absolute()

audio_concat = f'{root_dir}/files/' + str(uuid.uuid4()) + '.mp3'
input_audio_file_path = f'{root_dir}/files/' + str(uuid.uuid4()) + '.txt'

#command = f"ffmpeg -f -y concat -safe 0 -i {input_audio_file_path} -c copy {audio_concat}".split()

command = f"ffmpeg -y -i /Users/evgeny/Documents/kinolab/files/6495d734-c8ea-41d8-9288-4a2187b74f4f.mp3 -i /Users/evgeny/Documents/kinolab/files/fffd1b47-a919-485d-92a7-b9b2d9daa288.mp3 -filter_complex [0:a][1:a]concat=n=2:v=0:a=1 {audio_concat}".split()
subprocess.run(command)
            

