import requests
from settings import settings


def get_access_token():
    url = 'https://api.avito.ru/token/'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        response_data = response.json()
    else:
        print('Ошибка:', response.status_code, response.text)
        return
    access_token = response_data("access_token")
    return access_token