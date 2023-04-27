import requests
import json
from config import exchanges


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = (f"https://api.apilayer.com/exchangerates_data/convert?to={sym_key}&from={base_key}&amount={amount}")

        payload = {}

        headers = {
            "apikey": "r7iR9RCN09DXxAfunNkC0mnLRAR0SIQR"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        r = json.loads(response.content)

        q = r['info']

        new_price = q['rate'] * float(amount)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return round(new_price, 2)