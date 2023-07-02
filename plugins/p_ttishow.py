from bot import Bot
from pyrogram import Client, filters
from database.database import add_group

@Bot.on_message(filters.new_chat_members)
async def new_group(client, message):
    for member in message.new_chat_members:
        if member.id == client.get_me().id:
            await add_group(message.chat.id)
            await message.reply_text("Thanks for adding me!")
