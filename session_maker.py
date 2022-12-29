from pyrogram import Client, filters

api_id = 20886214
api_hash = "ba51cbd8e8f1dd0fce0d755ce0970600"

#for number in range(10,16):
pycl = Client(f"s10", api_id, api_hash)
pycl.start()    
pycl.stop()