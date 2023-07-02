from bot import Bot
from pyrogram import Client, filters

@Bot.on_message(filters.new_chat_members)
async def new_group(client, message):
    for member in message.new_chat_members:
        if member.id == client.get_me().id:
   
            await message.reply_text("Thanks for adding me!")￼Enter
