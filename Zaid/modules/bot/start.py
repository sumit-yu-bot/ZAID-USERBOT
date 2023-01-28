from Zaid import app
from pyrogram import filters


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
   await message.reply_text("𝐇𝐞𝐲 𝐙𝐚𝐢𝐝 𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐡𝐞𝐫𝐞")
