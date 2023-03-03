import subprocess, time, uuid, sys, os, random, traceback
from utils import TerminalColors, MetaData
from pathlib import Path


class VideoCombiner:

    @staticmethod
    def combine(task, video):
        
        try:

            time_start = time.time()

            root_dir = Path().absolute()

            video_file_path = video
            intro_file_path = f'{root_dir}/intro/intro.mp4'
            video_out = f'{root_dir}/files/' + str(uuid.uuid4()) + '.mp4'
            intro_out = f'{root_dir}/files/' + str(uuid.uuid4()) + '.mp4'
            intro_audio = f'{root_dir}/intro/' + str(random.randint(1,9)) + '.mp3'
            video_audio = f'{root_dir}/files/' + str(uuid.uuid4()) + '.mp3'
            audio_concat = f'{root_dir}/files/' + str(uuid.uuid4()) + '.mp3'

            video_concat_audio_file_path = f'{root_dir}/files/' + str(uuid.uuid4()) + '.mp4'
            input_file_path = f'{root_dir}/files/' + str(uuid.uuid4()) + '.txt'
            meta = MetaData.get(video_file_path)

            tbn = meta['time_base'].split('/')[1]
            ratio = f"{meta['coded_width']}:{meta['coded_height']}"
            avg_frame_rate = meta['avg_frame_rate'].split('/')[0]
            wh = ratio.split(':')

            subprocess.run(f'ffmpeg -y -i {intro_file_path} -vf scale={ratio}:force_original_aspect_ratio=decrease,pad={ratio}:-1:-1:color=black -vsync 2 -video_track_timescale {tbn} {intro_out}'.split())
            
            meta_one = MetaData.get(video_file_path)
            meta_two = MetaData.get(intro_out)


            for key in meta_one.keys():
                try:
                    if meta_one[key] != meta_two[key]:
                        print(TerminalColors.OKBLUE + f"{key}:\n       {str(meta_one[key])}\n" + TerminalColors.ENDC + TerminalColors.FAIL + "       " + str(meta_two[key]) + TerminalColors.ENDC)
                    else:
                        print(TerminalColors.OKBLUE + f"{key}:\n       {str(meta_one[key])}\n" + TerminalColors.ENDC + TerminalColors.OKBLUE + "       " + str(meta_two[key]) + TerminalColors.ENDC )
                except Exception as e:
                    pass

            print(TerminalColors.OKBLUE + "GET AUDIO FROM FILM" + TerminalColors.ENDC)

            command = f"ffmpeg -y -i {video_file_path} -q:a 0 -map a {video_audio}".split()
            subprocess.run(command)

            print(TerminalColors.OKBLUE + "CONCAT AUDIOS" + TerminalColors.ENDC)

            command = f"ffmpeg -y -i {intro_audio} -i {video_audio} -filter_complex [0:a][1:a]concat=n=2:v=0:a=1 {audio_concat}"
            print(command)
            
            subprocess.run(command.split())
            

            print(audio_concat)


            print(TerminalColors.OKBLUE + "CONCAT VIDEO" + TerminalColors.ENDC)

            with open(input_file_path, 'w') as f:
                f.write(f"file '{intro_out}'\nfile '{video_file_path}'")

            command = f"ffmpeg -y -f concat -safe 0 -i {input_file_path} -c copy -movflags +faststart {video_out}".split()
            subprocess.run(command)
            print(TerminalColors.OKBLUE + "CONCAT VIDEO AND AUDIO" + TerminalColors.ENDC)

            command = f"ffmpeg -y -i {video_out} -i {audio_concat} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {video_concat_audio_file_path}".split()
            subprocess.run(command)
            

            time_end = round(time.time() - time_start)

            intro_file_path = f'{root_dir}/intro/intro.mp4'

            os.remove(video_out)
            os.remove(intro_out)
            os.remove(video_audio)
            os.remove(audio_concat)
            os.remove(video_file_path)
            os.remove(input_file_path)

            print('Combine videos time: ', time_end)

            time.sleep(2)



            return {
                'meta_after_combine': MetaData.get(video_concat_audio_file_path),
                'path': video_concat_audio_file_path,
                'audio_path': intro_audio
            }

        except Exception as e:
            traceback.print_exc()
            return False
