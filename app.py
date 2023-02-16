import requests
import telebot
import json

TOKEN = "5883210639:AAF7SNGvpxJSZgTUZ8fcNNLeHMpHC6gT9E4"

bot = telebot.TeleBot(TOKEN)

keys = {
    'биткойн': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
    'евро':'',
    'рубль':'',
    'юань':'',

}

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для конвертации валюты введите команду боту в формате: \n <имя валюты> <в какую валюту перевести> <колличество переводимой валюты> ' \
           '\n Список доступных валют: /values '
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'{amount} {base} в {quote} - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()
