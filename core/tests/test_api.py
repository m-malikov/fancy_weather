from typing import Dict, Optional

import pytest

from lib import api

pytest_plugins = 'aiohttp.pytest_plugin'

USER_MESSAGE = "Какая погода завтра?"
RESPONSE_TO_USER = {"text": "+18 градусов."}


class MockWeather:
    def __init__(self):
        pass

    @staticmethod
    async def process_message(message: str) -> Dict[str, Optional[str]]:
        if message == USER_MESSAGE:
            return RESPONSE_TO_USER


def create_app(test_client):
    weather = MockWeather()
    api_app = api.create_app(weather)
    return api_app


@pytest.mark.asyncio
async def test_ping(test_client):
    client = await test_client(create_app)
    resp = await client.get('/ping')
    assert resp.status == 200
    assert await resp.text() == "OK"


@pytest.mark.asyncio
async def test_weather_no_text(test_client):
    client = await test_client(create_app)
    resp = await client.get('/api/v1/weather')
    assert resp.status == 422
    assert await resp.text() == 'Send user text as query param'


@pytest.mark.asyncio
async def test_weather_empty_text(test_client):
    client = await test_client(create_app)
    resp = await client.get('/api/v1/weather?text=')
    assert resp.status == 422
    assert await resp.text() == 'Send user text as query param'


@pytest.mark.asyncio
async def test_weather_ok_text(test_client):
    client = await test_client(create_app)
    resp = await client.get(f'/api/v1/weather?text={USER_MESSAGE}')
    assert resp.status == 200
    assert await resp.json() == RESPONSE_TO_USER
