from telebot import TeleBot
from telebot.handler_backends import ContinueHandling


bot = TeleBot('6618622439:AAHSQRJM8sgN4ABxu1fm77QGy9UJg3ozTCY')

@bot.message_handler(commands=['command1','command2'])
def start(message):
    bot.send_message(message.chat.id, 'Hello World!')
    

@bot.message_handler(commands=['start'])
def start2(message):
    """
    This handler comes after the first one, but it will never be called.
    But you can call it by returning ContinueHandling() in the first handler.

    If you return ContinueHandling() in the first handler, the next 
    registered handler with appropriate filters will be called.
    """
    bot.send_message(message.chat.id, 'Hello World2!')

bot.infinity_polling()