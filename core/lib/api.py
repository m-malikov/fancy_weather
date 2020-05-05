from aiohttp import web

from lib.weather import Weather


class Handler:
    def __init__(self, weather: Weather) -> None:
        self._weather = weather

    @staticmethod
    async def ping(request: web.Request) -> web.Response:
        return web.Response(text='OK', status=200)

    async def api(self, request: web.Request) -> web.Response:
        params = request.rel_url.query
        text = params.get('text')
        if text is None:
            return web.Response(text='Send user text as query param', status=422)

        result = await self._weather.process_message(text)
        return web.json_response(data=result, status=200)


def create_app(weather: Weather) -> web.Application:
    app = web.Application()

    handler = Handler(weather)
    app.add_routes([
        web.get('/ping', handler.ping),
        web.get('/api/v1/weather', handler.api)
    ])

    return app
