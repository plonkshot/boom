import logging
from telethon import TelegramClient, events
import os
import asyncio
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | 📝 %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("DragonUserbot")

api_id = 22997392
api_hash = "8202a02ab5ecd8000e40eec6183f676b"

BLACKLIST_FILE = 'blacklist.txt'

client = TelegramClient('bot', api_id, api_hash)

autogcast_task = None
autogcast_message = None

def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        return set()
    with open(BLACKLIST_FILE, 'r') as file:
        return set(line.strip() for line in file)

def save_blacklist(blacklist):
    with open(BLACKLIST_FILE, 'w') as file:
        for item in blacklist:
            file.write(f"{item}\n")

blacklist = load_blacklist()

@client.on(events.NewMessage(pattern='/gcast'))
async def gcast_handler(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        async for dialog in client.iter_dialogs():
            if dialog.is_group and str(dialog.id) not in blacklist:
                try:
                    await client.forward_messages(dialog.id, reply_message)
                    logger.info(f"📤 Pesan berhasil dikirim ke grup: {dialog.name}")
                except Exception as e:
                    logger.error(f"⚠️ Gagal mengirim pesan ke grup {dialog.name}: {e}")
        await event.reply("✅ Broadcast selesai!")
    else:
        await event.reply("❌ Mohon reply ke pesan yang ingin di-broadcast.")

@client.on(events.NewMessage(pattern='/addbl'))
async def addbl_handler(event):
    if event.is_group:
        blacklist.add(str(event.chat_id))
        save_blacklist(blacklist)
        await event.reply("🚫 Grup telah ditambahkan ke blacklist broadcast.")
        logger.info(f"🔒 Grup {event.chat_id} ditambahkan ke blacklist.")
    else:
        await event.reply("❌ Perintah hanya bisa digunakan dalam grup.")

@client.on(events.NewMessage(pattern='/autogcast'))
async def autogcast_handler(event):
    global autogcast_task, autogcast_message

    if event.is_reply:
        autogcast_message = await event.get_reply_message()
        match = re.search(r'(\d+)(menit|jam)', event.raw_text.lower())
        if not match:
            await event.reply("❌ Format tidak valid! Contoh: `/autogcast 30menit` atau `/autogcast 1jam`")
            return

        duration = int(match.group(1))
        unit = match.group(2)
        interval = duration * 60 if unit == "menit" else duration * 3600

        if autogcast_task:
            autogcast_task.cancel()

        autogcast_task = asyncio.create_task(autogcast(interval))
        await event.reply(f"⏳ Autogcast akan berjalan setiap {duration} {unit}.")
    else:
        await event.reply("❌ Mohon reply ke pesan yang ingin di-broadcast secara otomatis.")

async def autogcast(interval):
    while True:
        async for dialog in client.iter_dialogs():
            if dialog.is_group and str(dialog.id) not in blacklist:
                try:
                    await client.forward_messages(dialog.id, autogcast_message)
                    logger.info(f"🔄 Autogcast terkirim ke grup: {dialog.name}")
                except Exception as e:
                    logger.error(f"⚠️ Gagal mengirim autogcast ke grup {dialog.name}: {e}")
        await asyncio.sleep(interval)

@client.on(events.NewMessage(pattern='/grouplist'))
async def grouplist_handler(event):
    group_list = []

    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            group_name = dialog.name
            group_entity = dialog.entity
            group_username = getattr(group_entity, 'username', None)
            link = f"@{group_username}" if group_username else "(tidak ada tautan)"
            group_list.append(f"📌 {len(group_list) + 1}. {group_name} {link}")

    if not group_list:
        await event.reply("❌ Tidak ada grup yang ditemukan.")
        return

    split_messages = []
    temp_message = "📋 **Daftar Grup**\n\n"
    for entry in group_list:
        if len(temp_message) + len(entry) + 1 > 4096:
            split_messages.append(temp_message)
            temp_message = ""
        temp_message += entry + "\n"
    if temp_message:
        split_messages.append(temp_message)

    for message in split_messages:
        await event.reply(message)

with client:
    logger.info("🚀 Userbot sedang berjalan...")
    client.run_until_disconnected()
