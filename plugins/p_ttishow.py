import datetime
import time
import asyncio

from bot import Bot
from pyrogram import Client, filters
from database.database import add_group, full_userbase, total_chat_count, get_all_chats
from config import ADMINS

@Bot.on_message(filters.new_chat_members)
async def new_group(client, message):
    for member in message.new_chat_members:
        if member.id == client.get_me().id:
            await add_group(message.chat.id)
            await message.reply_text("Thanks for adding me!")



@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def grp_brodcst(bot, message):
    chats = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    total_chats = await db.total_chat_count()
    done = 0
    failed =0

    success = 0
    async for chat in chats:
        pti, sh = await broadcast_messages(chat['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Chats {total_chats}\nCompleted: {done} / {total_chats}\nSuccess: {success}\nFailed: {failed}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Chats {total_chats}\nCompleted: {done} / {total_chats}\nSuccess: {success}\nFailed: {failed}")


async def broadcast_messages(chat_id, message):
    try:
        await message.copy(chat_id=chat_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(chat_id, message)
    except InputUserDeactivated:
        return False, "Deleted"
    except UserIsBlocked:
        return False, "Blocked"
    except PeerIdInvalid:
        return False, "Error"
    except Exception as e:
        return False, "Error"
