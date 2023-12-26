import time
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
import openai

openai.api_key = Config.OPENAI_API

@Client.on_message(filters.private & filters.text & ~filters.command)
async def ai_answer(client, message):
    if Config.AI:
        user_id = message.from_user.id

        try:
            users_message = message.text
            response = make_openai_request(users_message)
            
            lazy_users_message = users_message
            lazy_response = response.choices[0].text
            
            btn = [
                [InlineKeyboardButton(text="⇱🤷‍♀️ Take Action 🗃️⇲", url=f'https://t.me/Graph_Star_Bot')],
                [InlineKeyboardButton(text="🗑 Delete log ❌", callback_data='close')],
            ]
            reply_markup = InlineKeyboardMarkup(btn)
            footer_credit = "**©️ [Star Bots Tamil](https://t.me/Star_Bots_Tamil)**"

            await client.send_message(
                Config.AI_LOGS,
                text=f"**⚡️⚡️#Star_AI_Query \n\n• A User Name :- {message.from_user.mention} with User ID :- `{user_id}`. Asked me This Query...\n\n══❚█══Q   U   E   R   Y══█❚══\n\n\n[Query]{lazy_users_message}\n\n👇Here is What I Responded :-\n:-`{lazy_response}`\n\n\n❚═USER ID═❚═• `{user_id}` \n❚═USER Name═❚═• `{message.from_user.first_name}` \n\n🗃️**",
                parse_mode=enums.ParseMode.MARKDOWN, 
                reply_markup=reply_markup
            )
            await message.reply(f"**{lazy_response}\n\n{footer_credit}**", parse_mode=enums.ParseMode.MARKDOWN)

        except Exception as error:
            print(error)
            await message.reply_text(f'**Error :- {error}**')
    else:
        return

def make_openai_request(users_message):
    while True:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=users_message,
                temperature=0.5,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0.1,
                presence_penalty=0.0,
            )
            return response
        except openai.error.OpenAIError as e:
            if "Rate limit reached" in str(e):
                print("Rate limit reached. Retrying in 20 seconds...")
                time.sleep(20)
            else:
                raise
