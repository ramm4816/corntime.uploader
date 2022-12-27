import ffmpeg, subprocess, time
from utils import TerminalColors, MetaData

class VideoCombiner:

    @staticmethod
    def combine_videos(sio, task, intro, video):
                
        time_start = time.time()

        VIDEO = video
        VIDEO_OUT = "film_out.mp4"
        INTRO = intro
        INTRO_OUT = "intro_resized.mp4"

        meta = MetaData.get(VIDEO)

        tbn = meta['time_base'].split('/')[1]
        ratio = f"{meta['coded_width']}:{meta['coded_height']}"
        avg_frame_rate = meta['avg_frame_rate'].split('/')[0]
        wh = ratio.split(':')

        subprocess.run(f'ffmpeg -y -i {INTRO} -vf scale={ratio}:force_original_aspect_ratio=decrease,pad={ratio}:-1:-1:color=black -vsync 2 -video_track_timescale {tbn} {INTRO_OUT}'.split(' '))

        meta_one = MetaData.get(VIDEO)
        meta_two = MetaData.get(INTRO_OUT)

        subprocess.run("clear")

        for key in meta_one.keys():
            if meta_one[key] != meta_two[key]:
                print(TerminalColors.OKBLUE + f"{key}:\n       {str(meta_one[key])}\n" + TerminalColors.ENDC + TerminalColors.FAIL + "       " + str(meta_two[key]) + TerminalColors.ENDC)
            else:
                print(TerminalColors.OKBLUE + f"{key}:\n       {str(meta_one[key])}\n" + TerminalColors.ENDC + TerminalColors.OKBLUE + "       " + str(meta_two[key]) + TerminalColors.ENDC )

        print(TerminalColors.OKBLUE + "GET AUDIO FROM INTRO" + TerminalColors.ENDC)

        command = f"ffmpeg -y -i {INTRO_OUT} -q:a 0 -map a audio.mp3".split(' ')
        subprocess.run(command)

        print(TerminalColors.OKBLUE + "GET AUDIO FROM FILM" + TerminalColors.ENDC)

        command = f"ffmpeg -y -i {VIDEO} -q:a 0 -map a audio_1.mp3".split(' ')
        subprocess.run(command)

        print(TerminalColors.OKBLUE + "CONCAT AUDIOS" + TerminalColors.ENDC)

        command = f"ffmpeg -y -i audio.mp3 -i audio_1.mp3 -filter_complex [0:a][1:a]concat=n=2:v=0:a=1 out.mp3".split(' ')
        subprocess.run(command)
        
        print(TerminalColors.OKBLUE + "CONCAT VIDEOS" + TerminalColors.ENDC)

        input_filepath = f"input.txt"

        with open(input_filepath, 'w') as f:
            f.write(f"file '{INTRO_OUT}'\nfile '{VIDEO}'")

        command = f"ffmpeg -y -f concat -safe 0 -i {input_filepath} -c copy -movflags +faststart {VIDEO_OUT}".split(' ')
        subprocess.run(command)

        print(TerminalColors.OKBLUE + "CONCAT VIDEO AND AUDIO" + TerminalColors.ENDC)

        command = f"ffmpeg -y -i {VIDEO_OUT} -i out.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 result.mp4".split(' ')
        subprocess.run(command)

        time_end = round(time.time() - time_start)

        print('execute_time: ', time_end)



