import datetime
import time
import asyncio

from bot import Bot
from pyrogram import Client, filters
from database.database import add_group, full_userbase, total_chat_count, get_all_chats
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid, ChatAdminRequired
from config import ADMINS
from pyrogram.types import Message


@Bot.on_message(filters.new_chat_members)
async def new_group(client: Bot, message):
    for member in message.new_chat_members:
        me = await client.get_me()
        if member.id == me.id:
            await message.reply_text("Thanks for adding me!")


@Bot.on_message(filters.command('status') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    g_total = await total_chat_count()
    users = await full_userbase()
    await msg.edit(f"Total Users: `{len(users)}`\nTotal Groups: `{g_total}`")


@Bot.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def grp_brodcst(bot: Bot, message: Message):
    chats = await get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    total_chats = await total_chat_count()
    done = 0
    failed =0

    success = 0
    async for chat in chats:
        pti, sh = await broadcast_messages(chat['id'], b_msg)
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
