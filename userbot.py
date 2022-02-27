from telethon import *
from telethon.sessions import StringSession
import random
import json

file = open('config.json').read()
config = json.loads(file)

API_ID = config['API_ID']
API_HASH = config['API_HASH']
STRING_SESSION = config['STRING_SESSION']

client = TelegramClient(StringSession(STRING_SESSION), api_id, api_hash).start()

CHANNEL_ID = config['CHANNEL_ID']

COMMENT_TEXT = config['COMMENT_TEXT']

@client.on(events.NewMessage(chats=channel_id))
async def auto_comment(event):
    print('''
New Post!
    ''')
    await client.send_message(event.chat_id, random.choice(COMMENT_TEXT), comment_to=event.id)
    print('''
Commented!
    ''')

print('Started!')
client.run_until_disconnected()