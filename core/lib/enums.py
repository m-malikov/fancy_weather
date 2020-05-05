from enum import Enum


class Condition(Enum):
    """
    Weather description decoding code.
    https://yandex.ru/dev/weather/doc/dg/concepts/forecast-test-docpage/
    """
    CLEAR = "clear"
    PARTLY_CLOUDY = "partly-cloudy"
    CLOUDY = "cloudy"
    OVERCAST = "overcast"
    PARTLY_CLOUDY_AND_LIGHT_RAIN = "partly-cloudy-and-light-rain"
    PARTLY_CLOUDY_AND_RAIN = "partly-cloudy-and-rain"
    OVERCAST_AND_RAIN = "overcast-and-rain"
    OVERCAST_THUNDERSTORMS_WITH_RAIN = "overcast-thunderstorms-with-rain"
    CLOUDY_AND_LIGHT_RAIN = "cloudy-and-light-rain"
    OVERCAST_AND_LIGHT_RAIN = "overcast-and-light-rain"
    CLOUDY_AND_RAIN = "cloudy-and-rain"
    OVERCAST_AND_WET_SNOW = "overcast-and-wet-snow"
    PARTLY_CLOUDY_AND_LIGHT_SNOW = "partly-cloudy-and-light-snow"
    PARTLY_CLOUDY_AND_SNOW = "partly-cloudy-and-snow"
    OVERCAST_AND_SNOW = "overcast-and-snow"
    CLOUDY_AND_LIGHT_SNOW = "cloudy-and-light-snow"
    OVERCAST_AND_LIGHT_SNOW = "overcast-and-light-snow"
    CLOUDY_AND_SNOW = "cloudy-and-snow"

    RAIN_CONDITIONS = {PARTLY_CLOUDY_AND_LIGHT_RAIN, PARTLY_CLOUDY_AND_RAIN, OVERCAST_AND_RAIN,
                       OVERCAST_THUNDERSTORMS_WITH_RAIN, CLOUDY_AND_LIGHT_RAIN, OVERCAST_AND_LIGHT_RAIN,
                       CLOUDY_AND_RAIN}

    SNOWY_CONDITIONS = {OVERCAST_AND_WET_SNOW, PARTLY_CLOUDY_AND_LIGHT_SNOW, PARTLY_CLOUDY_AND_SNOW,
                        OVERCAST_AND_SNOW, CLOUDY_AND_LIGHT_SNOW, OVERCAST_AND_LIGHT_SNOW, CLOUDY_AND_SNOW}

    def translate_to_russian(self) -> str:
        if self == Condition.CLEAR:
            return "Ясно."

        if self == Condition.PARTLY_CLOUDY:
            return "Малооблачно."

        if self == Condition.CLOUDY:
            return "Облачно с прояснениями."

        if self == Condition.OVERCAST:
            return "Пасмурно."

        if self == Condition.PARTLY_CLOUDY_AND_LIGHT_RAIN:
            return "Небольшой дождь."

        if self == Condition.PARTLY_CLOUDY_AND_RAIN:
            return "Дождь."

        if self == Condition.OVERCAST_AND_RAIN:
            return "Сильный дождь."

        if self == Condition.OVERCAST_THUNDERSTORMS_WITH_RAIN:
            return "Сильный дождь, гроза."

        if self == Condition.CLOUDY_AND_LIGHT_RAIN:
            return "Небольшой дождь."

        if self == Condition.OVERCAST_AND_LIGHT_RAIN:
            return "Небольшой дождь."

        if self == Condition.CLOUDY_AND_RAIN:
            return "Дождь."

        if self == Condition.OVERCAST_AND_WET_SNOW:
            return "Дождь со снегом."

        if self == Condition.PARTLY_CLOUDY_AND_LIGHT_SNOW:
            return "Небольшой снег."

        if self == Condition.PARTLY_CLOUDY_AND_SNOW:
            return "Снег."

        if self == Condition.OVERCAST_AND_SNOW:
            return "Снегопад."

        if self == Condition.CLOUDY_AND_LIGHT_SNOW:
            return "Небольшой снег."

        if self == Condition.OVERCAST_AND_LIGHT_SNOW:
            return "Небольшой снег."

        if self == Condition.CLOUDY_AND_SNOW:
            return "Снег."

        return ""


class Season(Enum):
    """
    The time of year in this locality.
    https://yandex.ru/dev/weather/doc/dg/concepts/forecast-test-docpage/
    """
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"
    SPRING = "spring"


class WeatherType(Enum):
    """
    Possible weather type for pictures and poems
    """
    RAINY = 'rainy'
    SNOWY = 'snowy'
    COLD = 'cold'
    WARM = 'warm'

    SPRING = 'spring'
    AUTUMN = 'autumn'
