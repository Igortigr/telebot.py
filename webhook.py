import json

from config import token
from telebot import telebot, types
import requests

bot = telebot.TeleBot(token)
url = 'https://api.telegram.org/bot{token}/{method}'.format(
    token=token,
    method='deleteWebhook'
)

data = {'url':'https://functions.yandexcloud.net/d4enmcphpbeuemmb3cs6'}
r = requests.post(url, data=data)
print(r.json())
