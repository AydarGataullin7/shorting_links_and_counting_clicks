import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(url, token):

    parsed_url = urlparse(url)
    if 'vk.cc' not in parsed_url.netloc:
        return False

    key = parsed_url.path.lstrip('/')
    stats_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': '5.199'
    }

    response = requests.get(stats_url, params=params)
    response.raise_for_status()
    stats_response = response.json()

    return 'error' not in stats_response


def shorten_link(url_to_shorten, token):
    shorten_api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': token,
        'url': url_to_shorten,
        'v': '5.199'
    }

    response = requests.get(shorten_api_url, params=params)
    response.raise_for_status()
    api_response = response.json()

    if 'error' in api_response:
        error_msg = api_response['error'].get('error_msg')
        raise requests.exceptions.HTTPError(
            "Ошибка VK API: {0}".format(error_msg))

    short_url = api_response['response']['short_url']
    return short_url


def count_clicks(short_url, token):
    stats_api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    parsed_short_url = urlparse(short_url)
    key = parsed_short_url.path.lstrip('/')
    params = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': '5.199'
    }

    response = requests.get(stats_api_url, params=params)
    response.raise_for_status()
    stats_response = response.json()

    if 'error' in stats_response:
        error_msg = stats_response['error'].get('error_msg')
        raise requests.exceptions.HTTPError(
            "Ошибка VK API: {0}".format(error_msg))

    counted_clicks = stats_response['response']['stats'][0]['views']
    return counted_clicks


def main():
    load_dotenv()
    token = os.environ['VK_API_TOKEN']
    url_for_short = input('Введите ссылку: ')
    try:
        if is_shorten_link(url_for_short, token):
            views = count_clicks(url_for_short, token)
            print('Количество переходов по ссылке: ', views)
        else:
            short_link = shorten_link(url_for_short, token)
            print('Сокращенная ссылка: ', short_link)
    except requests.exceptions.HTTPError:
        print("Проверьте правильность введенной ссылки и настройки доступа.")


if __name__ == "__main__":
    main()
