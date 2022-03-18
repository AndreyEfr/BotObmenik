import json
import datetime
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup

TOKEN = '5242495347:AAG2ds4i2uE6S6eZcMLRvcET1qJVC9WbbE4'
print("Bot is up")
updater = Updater(TOKEN)

def loggin(a, b, c):
    l = str(datetime.datetime.now())
    memory_json = [
    {
        'first_name': a,
        'last_name': str(b),
        'action': c,
        'time': l
    }]
    print(a)
    with open("hist.json","a")as f:
        json.dump(memory_json, f, indent= 3)
    

def welcome(update, context):
    chat = update.effective_chat
    buttons = [[KeyboardButton('USD')], [KeyboardButton('EUR')], [KeyboardButton('PLN')], [KeyboardButton('SEK')]]
    context.bot.send_message(chat_id=chat.id, text='Hello! I am your currency bot',
                             reply_markup=ReplyKeyboardMarkup(buttons))


def currency_rate(update, context):
    chat = update.effective_chat
    currency_code = update.message.text
    if currency_code in ('USD', 'EUR', 'PLN', 'SEK'):
        currency_rate = requests.get(f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode='
                                     f'{currency_code}&date=20200302&json').json()
        rate = currency_rate[0]['rate']
        message = f'{currency_code} rate: {rate} UAH'
    a = update.message.chat.first_name
    b = update.message.chat.last_name
    f = loggin(a, b,currency_code)
    context.bot.send_message(chat_id=chat.id, text=message)
    context.bot.send_message(chat_id=chat.id, text=f)



disp = updater.dispatcher
disp.add_handler(CommandHandler('start', welcome))
disp.add_handler(MessageHandler(Filters.all, currency_rate))

updater.start_polling()
updater.idle()
