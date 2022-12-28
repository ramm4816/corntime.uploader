import subprocess, time, uuid, sys, os, random
from utils import TerminalColors, MetaData


def ppprint(string):
    string = string.strip()
    if "sp3333eed" in string:
        string = f"\n{string}"
        print(TerminalColors.WARNING + string + TerminalColors.ENDC, end='\r', file=sys.stdout, flush=True)


class VideoCombiner:



    @staticmethod
    def combine(client_socket_io, task, video):
        
        try:

            time_start = time.time()

            intro_file_path = 'intros/intro.mp4'
            video_file_path = video
            video_out = 'files/' + str(uuid.uuid4()) + '.mp4'
            intro_out = 'files/' + str(uuid.uuid4()) + '.mp4'
            intro_audio = 'into_audios/' + random.randint(1,9) + '.mp3'
            video_audio = 'files/' + str(uuid.uuid4()) + '.mp3'
            audio_concat = 'files/' + str(uuid.uuid4()) + '.mp3'
            video_concat_audio_file_path = 'files/' + str(uuid.uuid4()) + '.mp4'

            meta = MetaData.get(video_file_path)

            tbn = meta['time_base'].split('/')[1]
            ratio = f"{meta['coded_width']}:{meta['coded_height']}"
            avg_frame_rate = meta['avg_frame_rate'].split('/')[0]
            wh = ratio.split(':')


            process = subprocess.Popen(f'ffmpeg -y -i {intro_file_path} -vf scale={ratio}:force_original_aspect_ratio=decrease,pad={ratio}:-1:-1:color=black -vsync 2 -video_track_timescale {tbn} {intro_out}'.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                ppprint(line)

            meta_one = MetaData.get(video_file_path)
            meta_two = MetaData.get(intro_out)

            for key in meta_one.keys():
                if meta_one[key] != meta_two[key]:
                    print(TerminalColors.OKBLUE + f"{key}:\n       {str(meta_one[key])}\n" + TerminalColors.ENDC + TerminalColors.FAIL + "       " + str(meta_two[key]) + TerminalColors.ENDC)
                else:
                    print(TerminalColors.OKBLUE + f"{key}:\n       {str(meta_one[key])}\n" + TerminalColors.ENDC + TerminalColors.OKBLUE + "       " + str(meta_two[key]) + TerminalColors.ENDC )

            print(TerminalColors.OKBLUE + "GET AUDIO FROM FILM" + TerminalColors.ENDC)

            command = f"ffmpeg -y -i {video_file_path} -q:a 0 -map a {video_audio}".split()
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
            for line in process.stdout:
                ppprint(line)

            print(TerminalColors.OKBLUE + "CONCAT AUDIOS" + TerminalColors.ENDC)

            command = f"ffmpeg -y -i {intro_audio} -i {video_audio} -filter_complex [0:a][1:a]concat=n=2:v=0:a=1 {audio_concat}".split()
            subprocess.Popen(command)
            
            print(TerminalColors.OKBLUE + "CONCAT VIDEO" + TerminalColors.ENDC)

            input_filepath = f"input.txt"

            with open(input_filepath, 'w') as f:
                f.write(f"file '{intro_out}'\nfile '{video_file_path}'")

            command = f"ffmpeg -y -f concat -safe 0 -i {input_filepath} -c copy -movflags +faststart {video_out}".split()
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
            for line in process.stdout:
                ppprint(line)

            print(TerminalColors.OKBLUE + "CONCAT VIDEO AND AUDIO" + TerminalColors.ENDC)

            command = f"ffmpeg -y -i {video_out} -i {audio_concat} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {video_concat_audio_file_path}".split()
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
            for line in process.stdout:
                ppprint(line)

            time_end = round(time.time() - time_start)

            print('execute_time: ', time_end)

            os.remove(video_file_path)
            os.remove(video_out)
            os.remove(intro_out)
            os.remove(intro_audio)
            os.remove(video_audio)
            os.remove(audio_concat)

            return video_concat_audio_file_path

        except Exception as e:
            print(e)
            return False
