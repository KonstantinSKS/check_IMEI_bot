import os

from dotenv import load_dotenv

load_dotenv()


API_TOKEN_CHECK_URL = os.getenv('API_TOKEN_CHECK_URL')
GET_SERVICES_URL = os.getenv('GET_SERVICES_URL')
IMEI_CHECK_URL = os.getenv('IMEI_CHECK_URL')


class CheckHeadersConst(object):
    """Константа для работы с API-сервисом."""

    @staticmethod
    def headers(text: str) -> dict:
        return {
            'Authorization': f'Bearer {text}',
            'Accept-Language': 'en',
            'Content-Type': 'application/json',
        }
