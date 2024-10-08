from xml.etree import ElementTree

import requests


def get_usd_to_rub_rate():
    # Ссылка на курс валют с сайта ЦБР
    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    response = requests.get(url)

    # Проверяем, что запрос был успешным
    if response.status_code == 200:
        # Парсим XML-ответ
        tree = ElementTree.fromstring(response.content)

        # Проходим по всем валютам в ответе
        for currency in tree.findall("Valute"):
            char_code = currency.find("CharCode").text
            if char_code == "USD":
                value = currency.find("Value").text
                return float(value.replace(",", "."))  # Преобразуем значение к числу с плавающей точкой
    else:
        return None
