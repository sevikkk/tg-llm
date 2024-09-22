import os

from pyrogram import Client, filters

keys = open('tg_key.txt', 'r').readlines()
api_id = keys[0].strip()
api_hash = keys[1].strip()

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message()
def message_listener(client, message):
    if message.from_user is None:
       ufn, un = "-", "-"
    else:
       ufn, un = message.from_user.first_name, message.from_user.username
    print(f"Received Message: {message.chat.title} {message.chat.id} |{ufn} {un}| {message.text}")

app.run()
