import ffmpeg, subprocess
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKBLUE = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class VideoCombiner:

    def get_metadata(filename):
        metadata = ffmpeg.probe(filename)["streams"]
        for _metadata in metadata:
            if _metadata['tags']['handler_name']=="VideoHandler":
                return _metadata

    def combine_videos(self, intro, video):
                
        time_start = time.time()

        VIDEO = video
        VIDEO_OUT = "film_out.mp4"
        INTRO = intro
        INTRO_OUT = "intro_resized.mp4"

        meta = get_metadata(VIDEO)

        tbn = meta['time_base'].split('/')[1]
        ratio = f"{meta['coded_width']}:{meta['coded_height']}"
        avg_frame_rate = meta['avg_frame_rate'].split('/')[0]
        wh = ratio.split(':')

        subprocess.run(f'ffmpeg -y -i {INTRO} -vf scale={ratio}:force_original_aspect_ratio=decrease,pad={ratio}:-1:-1:color=black -vsync 2 -video_track_timescale {tbn} {INTRO_OUT}'.split(' '))

        m1 = get_metadata(VIDEO)
        m2 = get_metadata(INTRO_OUT)

        subprocess.run("clear")

        for key in m1.keys():
            if m1[key] != m2[key]:
                print(bcolors.OKBLUE + f"{key}:\n       {str(m1[key])}\n" + bcolors.ENDC + bcolors.FAIL + "       " + str(m2[key]) + bcolors.ENDC)
            else:
                print(bcolors.OKBLUE + f"{key}:\n       {str(m1[key])}\n" + bcolors.ENDC + bcolors.OKBLUE + "       " + str(m2[key]) + bcolors.ENDC )


        print(bcolors.OKBLUE + "GET AUDIO FROM INTRO" + bcolors.ENDC)


        command = f"ffmpeg -y -i {INTRO_OUT} -q:a 0 -map a audio.mp3".split(' ')
        subprocess.run(command)

        print(bcolors.OKBLUE + "GET AUDIO FROM FILM" + bcolors.ENDC)

        command = f"ffmpeg -y -i {VIDEO} -q:a 0 -map a audio_1.mp3".split(' ')
        subprocess.run(command)

        print(bcolors.OKBLUE + "CONCAT AUDIOS" + bcolors.ENDC)

        command = f"ffmpeg -y -i audio.mp3 -i audio_1.mp3 -filter_complex [0:a][1:a]concat=n=2:v=0:a=1 out.mp3".split(' ')
        subprocess.run(command)

        print(bcolors.OKBLUE + "CONCAT VIDEOS" + bcolors.ENDC)

        input_filepath = f"input.txt"

        with open(input_filepath, 'w') as f:
            f.write(f"file '{INTRO_OUT}'\nfile '{VIDEO}'")

        command = f"ffmpeg -y -f concat -safe 0 -i {input_filepath} -c copy -movflags +faststart {VIDEO_OUT}".split(' ')
        subprocess.run(command)

        print(bcolors.OKBLUE + "CONCAT VIDEO AND AUDIO" + bcolors.ENDC)

        command = f"ffmpeg -y -i {VIDEO_OUT} -i out.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 result.mp4".split(' ')
        subprocess.run(command)

        time_end = round(time.time() - time_start)

        print('execute_time: ', time_end)



