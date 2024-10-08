import os
import datetime
import pickle
from datetime import datetime, timedelta
import asyncio

from pyrogram import Client, filters

keys = open('tg_key.txt', 'r').readlines()
api_id = keys[0].strip()
api_hash = keys[1].strip()

channel_id = "-1001822567201" #it poland

async def fetch_messages_in_date_range(client, channel_id, start_date, end_date, offset_id=0):
    messages = []
    i = 0
    async for msg in client.get_chat_history(channel_id, offset_id=offset_id):
        #print(f"Message ID: {msg.id}, Date: {msg.date}, Content: {msg.text}")
        if msg.date < start_date:
            break
        if start_date <= msg.date <= end_date:
            messages.append(msg)
        i += 1
        if i % 1000 == 0:
            print(msg.date)
    return messages


async def main():
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=24*90)
    offset_id = 0

    async with Client("my_account", api_id, api_hash) as app:
        messages = await fetch_messages_in_date_range(app, channel_id, start_date, end_date, offset_id)
        msgs_by_id = {m.id: m for m in messages}
        tops = {m.reply_to_message_id for m in messages if m.reply_to_message_id is not None}
        known_ids = set(msgs_by_id.keys())
        while True:
            unknown_ids = tops - known_ids
            if not unknown_ids:
                break
            print(f"fetching {len(unknown_ids)} additional messages {unknown_ids}")
            new_messages = await app.get_messages(channel_id, message_ids=unknown_ids)
            print(new_messages and len(new_messages))
            for msg in new_messages:
                msgs_by_id[msg.id] = msg
                if msg.reply_to_message_id:
                    tops.add(msg.reply_to_message_id)
                known_ids.add(msg.id)

        pickle.dump({"history": messages, "msgs": msgs_by_id}, open("data/messages.pkl", "wb"))

if __name__ == "__main__":
    asyncio.run(main())
