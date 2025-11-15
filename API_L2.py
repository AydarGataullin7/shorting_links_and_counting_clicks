import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
url_for_short = input('Введите ссылку: ')


def is_shorten_link(url):
    parsed_inputed_url = urlparse(url)
    return 'vk.cc' in parsed_inputed_url.netloc


def shorten_link(url_to_shorten):
    url_doing_short = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': os.getenv('token'),
        'url': url_to_shorten,
        'v': '5.199'
    }

    response = requests.get(url_doing_short, params=params)
    response.raise_for_status()
    response_data = response.json()

    if 'error' in response_data:
        error_msg = response_data['error'].get(
            'error_msg')
        raise requests.exceptions.HTTPError(
            "Ошибка VK API: {0}".format(error_msg))

    short_url = response_data['response']['short_url']
    return short_url


def count_clicks(short_url):
    url_cuonting_clicks = 'https://api.vk.ru/method/utils.getLinkStats'
    parsed_short_url = urlparse(short_url)
    key = parsed_short_url.path.lstrip('/')
    params = {
        'access_token': os.getenv('token'),
        'key': key,
        'interval': 'forever',
        'v': '5.199'
    }

    response = requests.get(url_cuonting_clicks, params=params)
    response.raise_for_status()
    response_info = response.json()

    if 'error' in response_info:
        error_msg = response_info['error'].get(
            'error_msg')
        raise requests.exceptions.HTTPError(
            "Ошибка VK API: {0}".format(error_msg))

    counted_clicks = response_info['response']['stats'][0]['views']
    return counted_clicks


def main():
    try:
        if is_shorten_link(url_for_short):
            views = count_clicks(url_for_short)
            print('Количество переходов по ссылке: ', views)
        else:
            short_link = shorten_link(url_for_short)
            print('Сокращенная ссылка: ', short_link)
    except requests.exceptions.HTTPError:
        print("Проверьте правильность введенной ссылки и настройки доступа.")


if __name__ == "__main__":
    main()
