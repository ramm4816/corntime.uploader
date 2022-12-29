import subprocess, os
import getpass
from pathlib import Path


dir = os.path.abspath(__file__).split('/install.')[0]


command = f'pip3 install -r requirements.txt'
#subprocess.run(command)

current_user = getpass.getuser()
print(current_user)
print(dir)


service_text = '''
Description=Uploader service
After=network-online.target

[Service]
User={current_user}
ExecStart=python3 /home/dev/uploader/uploader.py
Restart=on-failure
RestartSec=3
LimitNOFILE=8192

[Install]
WantedBy=multi-user.target
'''

#with open('/etc/systemd/system/uploader.service', 'w') as f:
#f.write(service_text)