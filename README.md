# pay-to-steam-telegram-bot
Telegram bot for pay to steam

Телеграм бот для пополнения steam кошелька в автоматическом режиме.
(Комментарии к коду и сам функционал написан на русском языке)


Запуск бота осуществляется с помощью файла main.py

В файле config.py указываются данные для подключения бота, и настройки его конфигурации(после их установки можно запускать бота)(Создать бота можно у https://t.me/BotFather)

В файле db.py реализована работа бота с базой данных в которой хранятся данные о пользователях.

В файле markups.py реализованы все кнопки и меню использующиеся в боте.

В файле qiwiapipay.py реализована работа бота с QIWI API.

database.db - база данных.

Для функционирования бота нужна установка дополнительных модулей: pyqiwip2p aiogram 

