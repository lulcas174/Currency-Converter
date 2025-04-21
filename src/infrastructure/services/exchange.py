import httpx
from decimal import Decimal
import os
from dotenv import load_dotenv

load_dotenv()


class ExchangeService:
    @staticmethod
    async def get_rates() -> dict:
        try:
            api_key = os.getenv("EXCHANGE_RATE_API_KEY")
            if not api_key:
                raise Exception("API key missing in .env")
            url = "https://api.apilayer.com/exchangerates_data/latest?base=EUR"
            headers = {"apikey": api_key}
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=25.0)
                data = response.json()
                if not data.get("success"):
                    raise Exception("Failed to fetch exchange rates")
                return data.get("rates", {})
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {str(e)}")

    @staticmethod
    async def calculate_rate(source: str, target: str) -> Decimal:
        rates = await ExchangeService.get_rates()
        if source not in rates or target not in rates:
            raise Exception("Invalid currency code")
        base_to_eur_rate = Decimal("1") / Decimal(str(rates[source]))
        eur_to_target_rate = Decimal(str(rates[target]))
        return base_to_eur_rate * eur_to_target_rate
