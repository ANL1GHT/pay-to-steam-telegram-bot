#import standart modules
import random
import re

#import special modules
from pyqiwip2p import QiwiP2P
from aiogram import Bot, Dispatcher, executor, types

#import internal modules
import config
import markups
from db import Database
import qiwiapipay as operationWithQIWI


"""Подключение бота"""
bot = Bot(token=config.TOKEN)
"""Подключение диспетчера бота"""
dispatcher = Dispatcher(bot)
"""Подключение базы данных"""
dataBase = Database("database.db")
"""Подключение аккаунта qiwi для приема p2p платежей"""
p2pAccount = QiwiP2P(auth_key=config.QIWI_TOKEN)

'''Генерация счета на оплату'''
async def amountGenerate(amount, message):
    if await check_amount(amount, message):
        print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
              f'Ввел сумму для оплаты:{amount} ')

        '''Инициализация суммы пополнения с коммисией, комментария к счету и самого счета на оплату'''
        amountWithCommission= int(float(amount)*config.COMMISION_FOR_USER)
        commentAmount = str(message.from_user.id) + "_" + str(random.randint(1, 9999))
        billForPay = p2pAccount.bill(amount=amountWithCommission, lifetime=15, comment=commentAmount)

        '''Запись чека в базу данных'''
        dataBase.add_check(message.from_user.id, amountWithCommission, billForPay.bill_id)

        await bot.send_message(message.from_user.id, f'<b>Данные об оплате:</b>\n'
                                                     f'<b>Cумма пополнения:</b> {amount} ₽\n '
                                                     f'<b>К оплате:</b> {amountWithCommission} ₽\n' 
                                                     f'<b>Ваш логин:</b> {dataBase.get_login_user(message.from_user.id)}\n'
                                                     f'<b>Кликнув по кнопке ниже ты перейдешь на сайт QIWI для оплаты</b>\n'
                                                     f'<b>Если хочешь сменить данные для пополнения нажми\n ▫️Пополнение стим▫️</b>',
                            reply_markup=markups.buy_menu(url=billForPay.pay_url, bill=billForPay.bill_id), parse_mode="html")

        print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
              f'Была создана ссылка для оплаты ')

        dataBase.set_a(message.from_user.id, False)

'''Функция проверки правильности суммы желаемой оплаты'''
async def check_amount(amount, message):
    if amount.isnumeric() is False:
        await bot.send_message(message.from_user.id, "Сумма пополнения должна быть числом")
        return False
    elif int(amount) < config.MIN_SUM_AMOUNT:
        await bot.send_message(message.from_user.id, text=f'Сумма пополнения должна быть не меньше {config.MIN_SUM_AMOUNT} рублей')
        return False
    elif int(amount) > config.MAX_SUM_AMOUNT:
        await bot.send_message(message.from_user.id, text=f'Сумма пополнения должна быть меньше {config.MAX_SUM_AMOUNT} рублей')
        return False
    return True

'''Вывод данных о пользователе(реализация кнопки "Профиль") '''
async def get_profile(message):
    await bot.send_message(message.from_user.id, text=f'<b>Твой профиль:</b>\n'
                                                      f'<b>Имя:</b> {message.from_user.first_name}\n'
                                                      f'<b>Steam логин:</b> {dataBase.get_login_user(message.from_user.id)}\n'
                                                      f'<b>ID:</b> {message.from_user.id}\n', parse_mode="html")

'''Функция проверки правильности логина'''
async def check_login(message):
    if (len(message.text) > 32) or (re.search(r'[^a-zA-Z0-9_]', message.text))  or (message.text.isnumeric()):
        await bot.send_message(message.from_user.id, "Неккоректный логин")
        return False
    else:
        return True

'''Функция расчета конвертируемых средств'''
async def convertate(money):

    '''money - рубли которые мы конвертируем, config.COMMISION - наша личная коммисия в процентах, rate_of_exchange() - возвращает коэффициент который равен отношению курса валют'''
    return float((money * (100-config.COMMISION)*0.01) * operationWithQIWI.rate_of_exchange(config.QIWI_TOKEN_API, "643", "398"))


'''Обработчик команды start'''
@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':

        print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
              f'Ввел /start')
        '''Запись нового юзера в базу данных'''
        if not dataBase.user_exists(message.from_user.id):
            dataBase.add_user(message.from_user.id)

        await bot.send_message(message.from_user.id, f'Привет, <b>{message.from_user.first_name}</b>\n'
                                                     f'Выбери что тебя интересует',
                               reply_markup=markups.main_menu(), parse_mode="html")

'''Обработчик команды help'''
@dispatcher.message_handler(commands=['help'])
async def help(message: types.Message):
    if message.chat.type == 'private':
        print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
              f'Ввел /help')
        await bot.send_message(message.from_user.id, f'<b>Оплата — только в рублях</b>\n'
                                                     f'<b>Где взять логин от Steam-аккаунта?</b>\n'
                                                     f'<b>Tут объяснение</b> — https://telegra.ph/Kak-uznat-svoj-login-v-Steam-12-16\n'
                                                     f'<b>Комиссия</b> — суммарная комиссия составляет {config.COMMISION_FOR_USER * 100 -100}%, также возможны комиссии банковских сервисов.\n'
                                                     f'<b>Ограничения</b> — минимальная сумма к пополнению составляет {config.MIN_SUM_AMOUNT}₽, максимальная — {config.MAX_SUM_AMOUNT}₽.\n'
                                                     f'<b>Внимание! Перед отправкой средств убедитесь в правильности написания вашего Steam логина</b>', parse_mode="html")


'''Обработчик всех сообщений от пользователя'''
@dispatcher.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':

        if message.text == "▫️Профиль▫️":
            '''Обработка нажатия кнопки "Профиль" '''
            print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
                  f'Нажал "Профиль" ')

            await get_profile(message)

        elif message.text == "▫️Информация▫️":
            '''Обработка нажатия кнопки "Информация" '''
            print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
                  f'Нажал "Информация" ')

            await help(message)

        elif message.text == "▫️Поддержка▫️":
            '''Обработка нажатия кнопки "Поддержка" '''
            print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
                  f'Нажал "Поддержка" ')

            await bot.send_message(message.from_user.id, text=f'<b>Перед обращением в поддержку прочитайте сначала раздел "Информация", если у вас есть вопросы - не прошла оплата, бот сломался и т.п. напишите мне:</b>\n\n'
                                                              f'{config.SUPPORT_ACCOUNT}', parse_mode="html")

        elif message.text == "▫️Пополнение стим▫️":
            '''Обработка нажатия кнопки "Пополнение стим" '''
            print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
                  f'Нажал "Пополнение стим" ')

            if dataBase.get_login_user(message.from_user.id) == "Не_указан":
                await bot.send_message(message.from_user.id, "Укажите ваш стим логин")
            else:
                await bot.send_message(message.from_user.id, text=f'<b>Ваш логин:</b> {dataBase.get_login_user(message.from_user.id)}\n'
                                                                  f'Хотите сменить его?',
                                       reply_markup=markups.changeLogin_menu(), parse_mode="html")

            dataBase.set_l(message.from_user.id, True)
            return
        elif dataBase.get_l(message.from_user.id) == True:
            if await check_login(message):
                print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
                      f'Ввел свой логин:{message.text} ')

                dataBase.set_login_user(message.from_user.id, message.text)

                dataBase.set_l(message.from_user.id, False)
                await bot.send_message(message.from_user.id, 'Введите сумму для пополнения')

                dataBase.set_a(message.from_user.id, True)
        elif dataBase.get_a(message.from_user.id) == True:
            await amountGenerate(message.text, message)

        else:
            print(f'USER:{message.from_user.first_name} ID: {message.from_user.id}\n'
                  f'Ввел {message.text} ')
            await bot.send_message(message.from_user.id, "Неизвестная команда")


'''Обработчик кнопки статуса оплаты'''
@dispatcher.callback_query_handler(text_contains="check_")
async def check(callback: types.CallbackQuery):
    bill = str(callback.data[6:])
    info = dataBase.get_check(bill)

    if info  != False:
        if str(p2pAccount.check(bill_id=bill).status) == "PAID": #Если статус p2p перевода - Оплачен

            user_money = int(info[2])
           # dataBase.set_money(callback.from_user.id, user_money)

            '''Операция конвертации валют'''
            operationWithQIWI.exchange(config.QIWI_TOKEN_API, await convertate(user_money), "398", config.ACCOUNT_NUMBER)

            '''Операция пополнения стим'''
            operationWithQIWI.pay_to_steam(dataBase.get_login_user(callback.from_user.id), await convertate(user_money), config.QIWI_TOKEN_API)

            '''Удаление чека'''
            dataBase.delete_check(bill_id=bill)
            #dataBase.set_money(callback.from_user.id, 0)
            await bot.send_message(callback.from_user.id, "Ваш счет пополнен, посмотреть баланс можно в профиле Steam")
        else:
            await bot.send_message(callback.from_user.id, "Вы не оплатили счет!")
    else:
        await bot.send_message(callback.from_user.id, "Счет не найден")

'''Обработчик кнопки "Да" при выборе смены логина'''
@dispatcher.callback_query_handler(text="change_yes")
async def change_yes(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, text="Укажите новый логин")

'''Обработчик кнопки "Нет" при выборе смены логина'''
@dispatcher.callback_query_handler(text="change_no")
async def change_no(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    dataBase.set_l(callback.from_user.id, False)
    await bot.send_message(callback.from_user.id, 'Введите сумму для пополнения')
    dataBase.set_a(callback.from_user.id, True)



'''Запуск'''
if __name__ == "__main__":
    print("Bot activation...")
    executor.start_polling(dispatcher, skip_updates=True)
    print("Bot ended")

