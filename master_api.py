import requests
from utils import TerminalColors


class MasterApi:

    @staticmethod
    def get_task():
        res = requests.get("https://fykp.ru/api/get_task_test?resource=start")
        print(TerminalColors.OKBLUE + res.text + '\n' + TerminalColors.ENDC)
        return res.json()

    @staticmethod
    def check_restart(host):
        res = requests.get("https://fykp.ru/api/check_restart")
        if res.text == "1":
            requests.get(f"https://api.telegram.org/bot6213721919:AAFKhp_8xVPguHsEfUkAdfars903EDzv7d0/sendMessage?chat_id=-1001865394041&text={host} restarting..")
        return True if res.text == "1" else False

    #test auto pull


    @staticmethod
    def update_task(task_id, channel_id, message_id, host, full_info):

        res = requests.post("https://fykp.ru/api/update_tasks", data={
            'message_id': message_id,
            'channel_id': channel_id,
            'task_id': task_id,
            'host': host,
            'info': full_info
        })

        print(res.text)

    @staticmethod
    def delete_source(task_id):
        res = requests.post("https://fykp.ru/api/delete_source", data={
            'task_id': task_id
        })
        print(res)