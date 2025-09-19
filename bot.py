# Environment Variable
from decouple import config

# telegram 
from telegram.ext import *
import telegram

# postgres module
from postgres import db

token=config('TOKEN')
updater = Updater(token)
dp = updater.dispatcher


class Telegram_Bot:
    def start_command(self, update, context):
        username = update.message.chat.username
        email = 'test@gmail.com'

        db.save(update.message.chat.id, 
                username,
                update.message.chat.first_name, 
                update.message.chat.last_name,
                update.message.photo, 
                update.message.chat.type, 
                email)
        update.message.reply_text(f"Hi {username}. How May i help you")

    def msg_reply(self, text:str):
        if 'hello' in text:
            return "How are you ?"
        if 'fine' in text:
            return 'Welcome !'
        if 'bye' in text:

            return 'Bye'
        else:
            return 'Sorry.. I did not understand'

    def msg_handler(self, update, context):
        type = update.message.chat.type
        text = str(update.message.text).lower()
        response = ''

        if type == 'group':
            if '@[channel_name]' in text:
                new_text = text.replace('@[channel_name]', '').strip()
                response = self.msg_reply(new_text)
        else:
            response = self.msg_reply(text)
        update.message.reply_text(response)


bot = Telegram_Bot()
dp.add_handler(CommandHandler('start', bot.start_command))
dp.add_handler(MessageHandler(Filters.text, bot.msg_handler))

updater.start_polling(1.0)
updater.idle()
