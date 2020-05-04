from tornado.options import define, parse_config_file


def init(config_path: str) -> None:
    """
    Define tornado.options and parse them from config defined by config_path
    """
    define("yandex_api_key", help="Api key to Yandex.Weather api", type=str)
    define("yandex_api_url",
           help="Url to Yandex.Weather api",
           type=str,
           default="https://api.weather.yandex.ru/v1/forecast?lat=55.75396&lon=37.620393&extra=true")

    define("db_uri", help="Uri to sqlite db", type=str, default="sqlite:///weather")

    define("weather_update_interval", help="How often to update weather from api in seconds", type=int, default=86400)

    define("host", help="default host to web server", type=str, default="localhost")
    define("port", help="http port for running configurator", type=int, default=5000)

    define("log_config_path", help="path to logging config as json", type=str)

    define("pictures_host", help="hostname of pictures service", type=str, default="localhost")
    define("pictures_port", help="port of pictures service", type=str, default=30600)
    define("pictures_api", help="api of pictures service", type=str, default="/generate/picture?weather=")

    define("poems_host", help="hostname of pictures service", type=str, default="localhost")
    define("poems_port", help="port of pictures service", type=str, default=30601)
    define("poems_api", help="api of pictures service", type=str, default="/?weather=")

    parse_config_file(config_path)

