import os

from dotenv import load_dotenv

load_dotenv()


API_TOKEN_CHECK_URL = os.getenv('API_TOKEN_CHECK_URL')
GET_SERVICES_URL = os.getenv('GET_SERVICES_URL')
IMEI_CHECK_URL = os.getenv('IMEI_CHECK_URL')

HELP_TEXT = ("Бот для проверки IMEI устройств.\n"
             "Авторизируйтесь по одному из API-токенов "
             "(API Sandbox или API Live).\n"
             "Бот проверит, подойдет ли ваш API-токен для использования "
             "на бесплатном сервисе по проверке IMEI устройств\n"
             "Если для токена не будет найден бесплатный сервис, "
             "то Бот предложит вам ввести другой токен.\n "
             "Для запуска или перезапуска бота нажмите /start"
             )


class CheckHeadersConst(object):
    """Константа для работы с API-сервисом."""

    @staticmethod
    def headers(text: str) -> dict:
        return {
            'Authorization': f'Bearer {text}',
            'Accept-Language': 'en',
            'Content-Type': 'application/json',
        }
