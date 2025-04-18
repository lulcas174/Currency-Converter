import requests
from decimal import Decimal

class ExchangeService:
    @staticmethod
    def get_rates() -> dict:
        response = requests.get(
            "http://api.exchangeratesapi.io/latest?base=EUR",
            headers={"apikey": ""}
        )
        data = response.json()
        return {
            "EUR": Decimal("1.0"),
            "USD": Decimal(str(data["rates"]["USD"])),
            "BRL": Decimal(str(data["rates"]["BRL"])),
            "JPY": Decimal(str(data["rates"]["JPY"]))
        }

    @staticmethod
    def calculate_rate(source: str, target: str) -> Decimal:
        rates = ExchangeService.get_rates()
        
        if source == "EUR":
            return rates[target]
            
        source_in_eur = Decimal("1") / rates[source]
        target_from_eur = rates[target]
        return source_in_eur * target_from_eur