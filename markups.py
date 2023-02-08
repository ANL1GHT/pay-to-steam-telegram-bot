from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton



'''Кнопка статуса оплаты'''
'''Inline'''
def buy_menu(isUrl=True, url="", bill=""):

    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        buttonUrlQIWI = InlineKeyboardButton(text="Ссылка на оплату", url=url)
        qiwiMenu.insert(buttonUrlQIWI)

    buttonCheckQIWI = InlineKeyboardButton(text="Проверить оплату", callback_data="check_" + bill)
    qiwiMenu.insert(buttonCheckQIWI)
    return qiwiMenu


'''Основное меню'''
'''Reply'''
def main_menu():

    buttonProfile = KeyboardButton(text="▫️Профиль▫️")
    buttonInfo = KeyboardButton(text="▫️Информация▫️")
    buttonSteamPay = KeyboardButton(text="▫️Пополнение стим▫️")
    buttonSupport = KeyboardButton(text="▫️Поддержка▫️")
    mainMenu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    mainMenu.insert(buttonProfile)
    mainMenu.insert(buttonInfo)
    mainMenu.insert(buttonSteamPay)
    mainMenu.insert(buttonSupport)
    return mainMenu


'''Кнопка смены ника'''
'''Inline'''
def changeLogin_menu():
    buttonChangeYes = InlineKeyboardButton(text="Да", callback_data="change_yes")
    buttonChangeNo = InlineKeyboardButton(text="Нет", callback_data="change_no")
    changeLoginMenu = InlineKeyboardMarkup(row_width=2)
    changeLoginMenu.insert(buttonChangeYes)
    changeLoginMenu.insert(buttonChangeNo)
    return changeLoginMenu

