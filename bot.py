import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

# Токен вашего бота
TOKEN = '7220815906:AAFw_nacPxVipWdsMC9H3nJ7r_ZEvMYjjwo'  # Ваш токен бота
bot = telebot.TeleBot(TOKEN)

# Подключаемся к Google Sheets API
CREDS_FILE = '/Users/ali/Downloads/credentials.json'
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=[
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
])
gc = gspread.authorize(creds)

# ID существующей Google Таблицы
SPREADSHEET_ID = '1R7Nl2k7XDtINA-PpQQj1KYP0_d4BzBZ_6LXTxDYx3o8'

# Открываем листы
sheet_ldsp = gc.open_by_key(SPREADSHEET_ID).worksheet('ЛДСП')
sheet_korobka = gc.open_by_key(SPREADSHEET_ID).worksheet('Коробка')
sheet_metal = gc.open_by_key(SPREADSHEET_ID).worksheet('Метал')
sheet_ldsp1 = gc.open_by_key(SPREADSHEET_ID).worksheet('ЛДСП1')
sheet_metal1 = gc.open_by_key(SPREADSHEET_ID).worksheet('Метал1')
sheet_korobka1 = gc.open_by_key(SPREADSHEET_ID).worksheet('Коробка1')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Основное меню с кнопками "Добавить" и "Забрать"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_add = KeyboardButton("Добавить")
    button_take = KeyboardButton("Забрать")
    markup.add(button_add, button_take)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Обработчик нажатий на кнопки "Добавить" и "Забрать"
@bot.message_handler(func=lambda message: message.text == "Добавить" or message.text == "Забрать")
def handle_buttons(message):
    if message.text == "Добавить":
        # Кнопки для добавления: ЛДСП, Коробка, Метал
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("ЛДСП"), KeyboardButton("Коробка"), KeyboardButton("Метал"), KeyboardButton("Назад"))
        bot.send_message(message.chat.id, "Что вы хотите добавить?", reply_markup=markup)
    elif message.text == "Забрать":
        # Кнопки для забора: ЛДСП З, Коробка З, Метал З
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("ЛДСП."), KeyboardButton("Коробка."), KeyboardButton("Метал."), KeyboardButton("Назад"))
        bot.send_message(message.chat.id, "Что вы хотите забрать?", reply_markup=markup)

# Функция для обработки множества пар "имя-количество"
def process_multiple_entries(sheet, message):
    try:
        entries = message.text.split()  # Разделяем сообщение по пробелам
        if len(entries) % 2 != 0:
            raise ValueError("Неверный формат, проверьте данные")

        # Цикл по парам (имя, количество)
        for i in range(0, len(entries), 2):
            name = entries[i]
            quantity = entries[i + 1]
            date = datetime.now().strftime('%d-%m-%Y')
            sheet.append_row([date, name, quantity])

        bot.send_message(message.chat.id, f"Данные успешно добавлены.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

# Обработчик добавления данных на ЛДСП
@bot.message_handler(func=lambda message: message.text == "ЛДСП")
def request_ldsp_data(message):
    bot.send_message(message.chat.id, "Введите данные в формате: Название Количество.")
    bot.register_next_step_handler(message, lambda msg: process_multiple_entries(sheet_ldsp, msg))

# Обработчик добавления данных на Коробка
@bot.message_handler(func=lambda message: message.text == "Коробка")
def request_korobka_data(message):
    bot.send_message(message.chat.id, "Введите данные в формате: Название Количество.")
    bot.register_next_step_handler(message, lambda msg: process_multiple_entries(sheet_korobka, msg))

# Обработчик добавления данных на Метал
@bot.message_handler(func=lambda message: message.text == "Метал")
def request_metal_data(message):
    bot.send_message(message.chat.id, "Введите данные в формате: Название Количество.")
    bot.register_next_step_handler(message, lambda msg: process_multiple_entries(sheet_metal, msg))

# Обработчик забора данных на ЛДСП1 (правильно сохраняет на ЛДСП1)
@bot.message_handler(func=lambda message: message.text == "ЛДСП.")
def request_ldsp1_data(message):
    bot.send_message(message.chat.id, "Введите данные в формате: Название Количество.")
    bot.register_next_step_handler(message, lambda msg: process_multiple_entries(sheet_ldsp1, msg))

# Обработчик забора данных на Коробка1 (правильно сохраняет на Коробка1)
@bot.message_handler(func=lambda message: message.text == "Коробка.")
def request_korobka1_data(message):
    bot.send_message(message.chat.id, "Введите данные в формате: Название Количество.")
    bot.register_next_step_handler(message, lambda msg: process_multiple_entries(sheet_korobka1, msg))

# Обработчик забора данных на Метал1 (правильно сохраняет на Метал1)
@bot.message_handler(func=lambda message: message.text == "Метал.")
def request_metal1_data(message):
    bot.send_message(message.chat.id, "Введите данные в формате: Название Количество.")
    bot.register_next_step_handler(message, lambda msg: process_multiple_entries(sheet_metal1, msg))

# Обработчик нажатия на кнопку "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_main_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Добавить"), KeyboardButton("Забрать"))
    bot.send_message(message.chat.id, "Вы вернулись в главное меню. Выберите действие:", reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)
