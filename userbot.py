from telethon import *
from telethon.sessions import StringSession
import random
import json

file = open('config.json').read()
config = json.loads(file)

API_ID = config['API_ID']
API_HASH = config['API_HASH']
STRING_SESSION = config['STRING_SESSION']

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH).start()

CHANNEL_ID = config['CHANNEL_ID']

COMMENT_TEXT = config['COMMENT_TEXT']

@client.on(events.NewMessage(chats=CHANNEL_ID))
async def auto_comment(event):
    print('''
New Post!
    ''')
    try: # for the post those doesn't have comments section or deleted amd such.
        await client.send_message(event.chat_id, random.choice(COMMENT_TEXT), comment_to=event.id)
        print('''
Commented!
    ''')

    except:
        pass

print('Started!')
client.run_until_disconnected()