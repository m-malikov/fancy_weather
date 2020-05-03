from aiohttp import web


async def ping_handler(request: web.Request):
    return web.Response(text='OK', status=200)


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes([
        web.get('/ping', ping_handler),
    ])

    return app
