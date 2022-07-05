import telebot
from conf import keys, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_c(message: telebot.types.Message):
    text = 'Бот умеет показывать цену определённого количества валюты (евро, доллара или рубля) в выбранных единицах. \n\n\
Формат: \n\
        <имя валюты, цену которой мы хотим узнать> <имя валюты для отображения цены> <количество валюты> \n\n\
Пример: \n\
        евро рубль 1000 \n\n\
Введите команду /values чтобы получить информацию о доступных валютах.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values_c = message.text.split(' ')

        if len(values_c) != 3:
            raise ConvertionException('Неверное количество параметров')

        base, quote, amount = values_c

        if base == quote:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        total_base = CryptoConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        return bot.reply_to(message, f'{e}')
    except Exception as e:
        return bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {base} в {quote} — {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()