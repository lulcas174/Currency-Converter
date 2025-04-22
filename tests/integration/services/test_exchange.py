import pytest
import httpx
from src.infrastructure.services.exchange import ExchangeService


@pytest.mark.asyncio
async def test_get_rates_success(mocker):
    mock_response = {
        "base": "EUR",
        "rates": {"USD": 1.2, "GBP": 0.9},
        "success": True
    }

    mock_client = mocker.patch("httpx.AsyncClient")

    async def mock_get(*args, **kwargs):
        return httpx.Response(200, json=mock_response)

    mock_client.return_value.__aenter__.return_value.get = mock_get

    rates = await ExchangeService.get_rates()

    assert "USD" in rates
    assert rates["USD"] == 1.2
    mock_client.assert_called_once()


@pytest.mark.asyncio
async def test_get_rates_api_failure(mocker):
    mock_response = {"success": False}
    mock_client = mocker.patch("httpx.AsyncClient")

    async def mock_get(*args, **kwargs):
        return httpx.Response(200, json=mock_response)

    mock_client.return_value.__aenter__.return_value.get = mock_get

    with pytest.raises(Exception) as exc_info:
        await ExchangeService.get_rates()
    assert "Failed to fetch exchange rates" in str(exc_info.value)


@pytest.mark.asyncio
async def test_calculate_rate_invalid_currency(mocker):
    mock_rates = {"USD": 1.2, "GBP": 0.9}
    mocker.patch.object(ExchangeService, 'get_rates', return_value=mock_rates)
    with pytest.raises(Exception) as exc_info:
        await ExchangeService.calculate_rate("EUR", "XYZ")
    assert "Invalid currency code" in str(exc_info.value)


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("EXCHANGE_RATE_API_KEY", raising=True)
    with pytest.raises(Exception) as exc_info:
        import asyncio
        asyncio.run(ExchangeService.get_rates())
    assert "API key missing" in str(exc_info.value)
