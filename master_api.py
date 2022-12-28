import requests
from utils import TerminalColors


class MasterApi:

    @staticmethod
    def get_task():
        res = requests.get("https://fykp.ru/api/get_task")
        print(TerminalColors.OKBLUE + res.text + '\n' + TerminalColors.ENDC)
        return res.json()

    @staticmethod
    def update_task(task_id, channel_id, message_id, host):
        requests.post("https://fykp.ru/api/update_tasks", data={
            'message_id': message_id,
            'channel_id': channel_id,
            'task_id': task_id,
            'host': host
        })