
import subprocess

intros = {
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
}

for intro in intros:
    intro_audio = f'intro_audios/{intro}.mp3'
    command = f"ffmpeg -y -i intros/{intro} -q:a 0 -map a {intro_audio}".split()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    for line in process.stdout:
        print(line)