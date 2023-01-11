import json

from config import token
from telebot import telebot, types
import requests

bot = telebot.TeleBot(token)
''' функция для подключания к облаку. Она остается неизменной'''
def handler(event, context):
    body = json.loads(event['body'])
    update = telebot.types.Update.de_json(body)
    bot.process_new_updates([update])

    '''
    будущие кнопки для режима 'разработчика'. Бот сможет принимать на вход голосовые партии и текст хвал. 
    На практике еще ничего не реализован
    '''
@bot.message_handler(commands=['developer'])
def button_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton(text='Добавить голосовую партию')
    item2 = types.KeyboardButton(text='Слова гимна')
    markup.row(item1, item2)
    bot.send_message(message.chat.id, 'что хотите сделать?', reply_markup=markup)

'''при 'worship' выскакивают кнопки "Слова гимна" / "Партия"'''
@bot.message_handler(commands=['worship'])
def button_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text="Слова гимна", callback_data='гимн')
    item2 = types.InlineKeyboardButton(text="Партия", callback_data='партия')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Что вас инетерсует?', reply_markup=markup)


@bot.message_handler(commands=['info_worship'])
def button_message(message):
    bot.send_message(message.chat.id,
                     'Меня зовут Алан. Моя цель облегчить жизнь духовного хора\nВот что я умею делать:'
                     '\n- Слова гимна\n'
                     '- Аудиозапись партии\nДля вызова команд, пропиши в чате \worship')


'''
При нажатии на кнопку 'Партия:' выскакиют другие кнопки с названиеми партий
    При нажатии на кнопку 'Слова гимна:' закгружатся гимны из облака, которые храняся в переменной img
'''

@bot.callback_query_handler(func=lambda call: True)
def back(call):
    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    if call.data == 'гимн':
        bot.send_message(call.message.chat.id, 'Слова гимна:')
        img = 'https://console.cloud.yandex.ru/folders/b1gtqq5mcu18s4s3t57f/storage/buckets/textchurch/ПЗ1_1.jpg'
        bot.send_photo(call.message.chat.id, img)
    elif call.data == 'партия':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton(text='🗣 Сопрано')
        item2 = types.KeyboardButton(text='🗣 Альт')
        item3 = types.KeyboardButton(text='🗣 Тенор')
        item4 = types.KeyboardButton(text='🗣 Бас')
        markup.row(item1, item2)
        markup.add(item3, item4)
        bot.send_message(call.message.chat.id, 'выберете вашу партию', reply_markup=markup)

'''Фукнция для принятия голосовых сообщений. Пока до конца не реализована'''
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))

    '''
    Обработчик сообщений. Бот выдает выбранную голосовую партию, хранящуюся в переменной audio.
    Здесь нужно написать путь из облака
    '''
@bot.message_handler(content_types=['text'])
def lesson_1(message):
    if message.text.lower() == '🗣 сопрано':
        audio = open(r'D:\Хвалы\Отчизна моя в небесах\Сопрано.ogg', 'rb')
        bot.send_message(message.chat.id, 'аудио сопрано')
        bot.send_audio(message.chat.id, audio)
        audio.close()
    elif message.text.lower() == '🗣 альт':
        audio = open(r'D:\Хвалы\Отчизна моя в небесах\Альт.ogg', 'rb')
        bot.send_message(message.chat.id, 'аудио альт')
        bot.send_audio(message.chat.id, audio)
        audio.close()
    elif message.text.lower() == '🗣 тенор':
        audio = open(r'D:\Хвалы\Отчизна моя в небесах\Тенор.ogg', 'rb')
        bot.send_message(message.chat.id, 'аудио тенора')
        bot.send_audio(message.chat.id, audio)
        audio.close()
    elif message.text.lower() == '🗣 бас':
        audio = open(r'D:\Хвалы\Отчизна моя в небесах\Бас.ogg', 'rb')
        bot.send_message(message.chat.id, 'аудио бас')
        bot.send_audio(message.chat.id, audio)
        audio.close()
    elif message.text == 'Л':
        text = '[хвалы на K](https://storage.yandexcloud.net/telegram-bot/textchurch/Yes and Amen (C).pdf)'
        bot.send_message(message.chat.id, text, parse_mode='MarkdownV2')
    elif message.text.lower() == 'добавить голосовую партию':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton(text='🗣 Сопрано')
        item2 = types.KeyboardButton(text='🗣 Альт')
        item3 = types.KeyboardButton(text='🗣 Тенор')
        item4 = types.KeyboardButton(text='🗣 Бас')
        markup.row(item1, item2)
        markup.add(item3, item4)
        bot.send_message(message.chat.id, 'выберете партию', reply_markup=markup)

#метод, чтобы бот работал постоянно. В облаке этой строки нет
bot.polling(none_stop=True)
