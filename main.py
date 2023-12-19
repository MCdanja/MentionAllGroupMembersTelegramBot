import json
from os import getenv, environ

from dotenv import load_dotenv
from pyrogram import Client, filters

load_dotenv()
api_id = getenv('API_ID')
api_hash = getenv('API_HASH')
TOKEN = getenv('BOT_TOKEN')

BOT_NAME = getenv('BOT_NAME')
ADMIN_IDS = json.loads(environ['ADMIN_IDS'])

bot = Client("MentionBot", api_id=api_id, api_hash=api_hash, bot_token=TOKEN)


@bot.on_message(filters.regex("^[@/#][aA][lL][lL]$") & filters.group)
async def mention_handler(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if user_id in ADMIN_IDS:
        chat_id = message.chat.id
        chat_members = bot.get_chat_members(chat_id)

        all_users_mention = []

        async for member in chat_members:
            if member.user.first_name != BOT_NAME:
                all_users_mention.append(member.user.mention)

        all_users_mention_text = ", ".join(all_users_mention)
        answer_text = f"Админ призывает вас: {all_users_mention_text}!"

    else:
        answer_text = 'Ты не можешь всех призвать, иди нахуй!!!'
        print(f'Этот человек попытался всех призвать: {user_name} - {user_id}')

    await message.reply(answer_text)


@bot.on_message(filters.command(["start"]))
async def mention_handler(client, message):
    user_id = message.from_user.id
    await message.reply(f'Твой айди в телеграме: {user_id}')

if __name__ == "__main__":
    bot.run()
