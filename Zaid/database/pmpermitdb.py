from Zaid.database import cli
import asyncio

collection = cli["Zaid"]["pmpermit"]

PMPERMIT_MESSAGE = (
    "╔════════════════════╗\n"
    "     ⛑ 𝗔𝗧𝗧𝗘𝗡𝗧𝗜𝗢𝗡 𝗣𝗟𝗘𝗔𝗦𝗘 ⛑\n"
    "╚════════════════════╝\n"
    "•ɪ'ᴍ ꜱᴜᴍɪᴛ ᴜꜱᴇʀʙᴏᴛ ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ᴍʏ ᴍᴀꜱᴛᴇʀ ꜰʀᴏᴍ ꜱᴘᴀᴍᴍᴇʀꜱ \n"
    "•ɪꜰ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ꜱᴘᴀᴍᴍᴇʀ ᴛʜᴇɴ ᴘʟᴢ ᴡᴀɪᴛ!\n"
    "•ᴜɴᴛɪʟ ᴛʜᴇɴ, ᴅᴏɴ'ᴛ ꜱᴘᴀᴍ, ᴏʀ ʏᴏᴜ'ʟʟ ɢᴇᴛ ʙʟᴏᴄᴋᴇᴅ ᴀɴᴅ ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ ᴍᴇ, ꜱᴏ ʙᴇ ᴄᴀʀᴇꜰᴜʟʟ ᴛᴏ ꜱᴇɴᴅ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇꜱ! \n"
    "╔════════════════════╗\n"
    "   !⚠️𝐘𝐎𝐔𝐑 𝐃𝐀𝐃𝐃𝐘 𝐒𝐔𝐌𝐈𝐓 -𝗨𝘀𝗲𝗿𝗕𝗼𝘁\n"
    "╚════════════════════╝\n"
)

BLOCKED = "**ʙꜱᴅᴋ ʙᴏʟᴀ ᴛʜᴀ ɴᴀ ʀᴜᴋ ᴊᴀᴀ!, ʙʟᴏᴄᴋ ʜᴏ ɢʏᴀ ɴᴀ!**"

LIMIT = 5


async def set_pm(value: bool):
    doc = {"_id": 1, "pmpermit": value}
    doc2 = {"_id": "Approved", "users": []}
    r = await collection.find_one({"_id": 1})
    r2 = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": 1}, {"$set": {"pmpermit": value}})
    else:
        await collection.insert_one(doc)
    if not r2:
        await collection.insert_one(doc2)


async def set_permit_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}})


async def set_block_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"block_message": text}})


async def set_limit(limit):
    await collection.update_one({"_id": 1}, {"$set": {"limit": limit}})


async def get_pm_settings():
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message


async def allow_user(chat):
    doc = {"_id": "Approved", "users": [chat]}
    r = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": "Approved"}, {"$push": {"users": chat}})
    else:
        await collection.insert_one(doc)


async def get_approved_users():
    results = await collection.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []


async def deny_user(chat):
    await collection.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})


async def pm_guard():
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    if not result["pmpermit"]:
        return False
    else:
        return True
