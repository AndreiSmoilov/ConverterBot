import requests
import json
from config import exchanges


class APIException(Exception):
    pass
class Convertor:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        if quote_key == base_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base_key}&symbols={sym_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][base_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {quote} в {sym} : {new_price}"
        return message