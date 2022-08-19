from telethon import *
from telethon.sessions import StringSession
import random
import json
import time
import re

file_1 = open('config.json').read()
config = json.loads(file_1)
file_2 = open('lang.json', encoding='utf-8').read()
lang = json.loads(file_2)

API_ID = config['API_ID']
API_HASH = config['API_HASH']
STRING_SESSION = config['STRING_SESSION']

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH).start()

client.parse_mode = 'html'

COMMENT_TEXT = config['COMMENT_TEXT']

_lang = config['LANGUAGE']
lang = lang[_lang]

def CONFIG_FUNC():
    file = open('config.json')
    read = file.read()
    j = json.loads(read)
    file.close()
    return j

global CHANNEL_ID
CHANNEL_ID = CONFIG_FUNC()['CHANNEL_ID']

def add_channel_id(channel_id):
    file = open('config.json', 'r')
    read = file.read()
    file.close()
    j = json.loads(read)
    if not str(channel_id).startswith('-100'):
        channel_id = f'-100{channel_id}'
    j['CHANNEL_ID'].append(channel_id)
    j = json.dumps(j, sort_keys=True, indent=4)
    file = open('config.json', 'w')
    file.write(j)
    file.close()

def remove_channel_id(channel_id):
    file = open('config.json', 'r')
    read = file.read()
    file.close()
    j = json.loads(read)
    if not str(channel_id).startswith('-100'):
        channel_id = f'-100{channel_id}'
    j['CHANNEL_ID'].remove(int(channel_id))
    j = json.dumps(j, sort_keys=True, indent=4)
    file = open('config.json', 'w')
    file.write(j)
    file.close()

@client.on(events.NewMessage(pattern='^\.(start|alive)', incoming=False))
async def start(event):
    await event.edit(lang['START_MSG'])

@client.on(events.NewMessage(pattern='^\.help', incoming=False))
async def help_msg(event):
    await event.edit(lang['HELP_MSG'])

@client.on(events.NewMessage(pattern='^\.features', incoming=False))
async def all_features(event):
    await event.edit(lang['FEATURES'])

@client.on(events.NewMessage(pattern='^\.commands', incoming=False))
async def total_commands(event):
    await event.edit(lang['TOTAL_COMMANDS'])

@client.on(events.NewMessage(pattern='^\.add', incoming=False))
async def add_channel_id_for_auto_comment(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        try:
            chat = await client.get_entity(reply_msg.from_id.channel_id)
        except:
            await event.edit(lang['REPLY_TO_CHANNEL_MSG_1'])
            return
        chat.id = int(f'-100{chat.id}')
        if chat.id in CONFIG_FUNC()['CHANNEL_ID']:
            await event.edit(lang['CHANNEL_ID_ALREADY_ADDED'])
            return
        else:
            add_channel_id(chat.id)
            CHANNEL_ID.append(chat.id)
            await event.edit(lang['ADDED_CHANNEL_ID'])
    else:
        regex = re.search('^\.add ?(.+)?', event.raw_text)
        if regex:
            try:
                try:
                    chat = await client.get_entity(int(regex.group(1)))
                except:
                    chat = await client.get_entity(str(regex.group(1)))
            except:
                await event.edit(lang['CHANNEL_ID_NOT_INVALID'])
                return
            chat.id = int(f'-100{chat.id}')
            if chat.id in  CONFIG_FUNC()['CHANNEL_ID']:
                await event.edit(lang['CHANNEL_ID_ALREADY_ADDED'])
                return
            else:
                add_channel_id(chat.id)
                CHANNEL_ID.append(chat.id)
                await event.edit(lang['ADDED_CHANNEL_ID'])

@client.on(events.NewMessage(pattern='^\.remove', incoming=False))
async def remove_channel_id_for_auto_comment(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        try:
            chat = await client.get_entity(reply_msg.from_id.channel_id)
        except:
            await event.edit(lang['REPLY_TO_CHANNEL_MSG_3'])
            return
        chat.id = int(f'-100{chat.id}')
        if not chat.id in  CONFIG_FUNC()['CHANNEL_ID']:
            await event.edit(lang['CHANNEL_ID_NOT_EXIST'])
            return
        else:
            remove_channel_id(chat.id)
            CHANNEL_ID.remove(chat.id)
            await event.edit(lang['REMOVED_CHANNEL_ID'])
    else:
        regex = re.search('^\.remove ?(.+)?', event.raw_text)
        if regex:
            try:
                try:
                    chat = await client.get_entity(int(regex.group(1)))
                except:
                    chat = await client.get_entity(str(regex.group(1)))
            except:
                await event.edit(lang['CHANNEL_ID_NOT_INVALID'])
                return
            chat.id = int(f'-100{chat.id}')
            if not chat.id in  CONFIG_FUNC()['CHANNEL_ID']:
                await event.edit(lang['CHANNEL_ID_NOT_EXIST'])
                return
            else:
                remove_channel_id(chat.id)
                CHANNEL_ID.remove(chat.id)
                await event.edit(lang['REMOVED_CHANNEL_ID'])

@client.on(events.NewMessage(pattern='^\.id', incoming=False))
async def getID(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        try:
            await event.edit(f'<b>ID:</b> <code>{reply_msg.from_id.channel_id}</code>')
        except:
            await event.edit(lang['REPLY_TO_CHANNEL_MSG_1'])
    else:
        regex = re.search('^\.id ?(.+)?', event.raw_text)
        if regex:
            if regex.group(1) is None:
                await event.edit(lang['ID_USAGE'])
                return
            try:
                try:
                    chat = await client.get_entity(int(regex.group(1)))
                except:
                    chat = await client.get_entity(str(regex.group(1)))
            except:
                await event.edit(lang['INVALID'])
                return
            await event.edit(f'<b>ID:</b> <code>-100{chat.id}</code>')

@client.on(events.NewMessage(pattern='^\.setlang', incoming=False))
async def set_language(event):
    regex = re.search('^\.setlang ?(.+)?', event, re.DOTALL)
    if regex:
        if regex.group(1):
            lang = regex.group(1)
            if not lang in CONFIG_FUNC['AVAILABLE_LANGUAGES']:
                await event.edit(lang['LANG_NOT_AVAILABLE'])
                return
            else:
                setLANGUAGE(lang)
                await event.edit(lang['LANG_SETTED'])
    else:
        await event.edit(lang['SETLANG_USAGE'])

@client.on(events.NewMessage)
async def _auto_comment(event):
    if event.chat_id not in CHANNEL_ID:
        return
    print(lang['NEW_POST'].format(event.peer_id.channel_id))
    try: # for the post those doesn't have comments section or deleted and such.
        await client.send_message(event.chat_id, random.choice(COMMENT_TEXT), comment_to=event.id)
        print(lang['COMMENTED'].format(event.peer_id.channel_id))
    except errors.FloodWaitError as e:
        print(lang['FLOOD_WAIT_ERROR'].format(e.seconds))
        time.sleep(e.seconds)
    except Exception as e:
        print(lang['ERROR_WHILE_POSTING'] + '\n' + e)

print(lang['STARTED_USERBOT'])
client.run_until_disconnected()
