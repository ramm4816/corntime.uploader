from pyrogram import Client
import uuid

api_id = 20886214
api_hash = "ba51cbd8e8f1dd0fce0d755ce0970600"

pycl = Client(str(uuid.uuid4()), api_id, api_hash)
pycl.start()    
pycl.stop()

