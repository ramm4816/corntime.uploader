import subprocess, os
import getpass
from pathlib import Path
 
dir = Path().absolute()

command = f'sudo apt install python3-pip'.split()
subprocess.run(command)
command = f'sudo pip3 install -r requirements.txt'.split()
subprocess.run(command)
command = f'sudo apt install ffmpeg'.split()
subprocess.run(command)
command = f'pip3 install python-socketio[client]'.split()
subprocess.run(command)

current_user = getpass.getuser()

service_text = f'''
Description=Uploader service
After=network-online.target

[Service]
User={current_user}
ExecStart=/usr/bin/python3 {dir}/app.py
WorkingDirectory={dir}
Restart=on-failure
RestartSec=3
LimitNOFILE=8192
[Install]
WantedBy=multi-user.target
'''


with open('/etc/systemd/system/uploader.service', 'w') as f:
    f.write(service_text)

command = 'sudo systemctl enable uploader.service'.split()
subprocess.run(command)

command = 'sudo service uploader start'.split()
subprocess.run(command)

print('.')