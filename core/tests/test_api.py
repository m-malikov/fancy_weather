# flake8: noqa

import pytest

from lib import api


@pytest.mark.asyncio
async def test_ping():
    api_app = api.create_app(None)
    assert True
