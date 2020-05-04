from enum import Enum


class Condition(Enum):
    """
    Weather description decoding code.
    https://yandex.ru/dev/weather/doc/dg/concepts/forecast-test-docpage/
    """
    CLEAR = "clear"
    PARTLY_CLOUDLY = "partly-cloudy"
    CLOUDLY = "cloudly"
    OVERCAST = "overcast"
    PARTLY_CLOUDLY_AND_LIGHT_RAIN = "partly-cloudy-and-light-rain"
    PARTLY_CLOUDLY_AND_RAIN = "partly-cloudy-and-ra in"
    OVERCAST_AND_RAIN = "overcast-and-rain"
    OVERCAST_THUNDERSTROMS_WITH_RAIN = "overcast-thunderstorms-with-rain"
    CLOUDLY_AND_LIGHT_RAIN = "cloudy-and-light-rain"
    OVERCAST_AND_LIGHT_RAIN = "overcast-and-light-rain"
    CLOUDLY_AND_RAIN = "cloudy-and-rain"
    OVERCAST_AND_WET_SNOW = "overcast-and-wet-snow"
    PARTLY_CLOUDLY_AND_LIGHT_SNOW = "partly-cloudy-and-light-snow"
    PARTLY_CLOUDLY_AND_SNOW = "partly-cloudy-and-snow"
    OVERCAST_AND_SNOW = "overcast-and-snow"
    CLOUDLY_AND_LIGHT_SNOW = "cloudy-and-light-snow"
    OVERCAST_AND_LIGHT_SNOW = "overcast-and-light-snow"
    CLOUDLY_AND_SNOW = "cloudy-and-snow"

    RAIN_CONDITIONS = {PARTLY_CLOUDLY_AND_LIGHT_RAIN, PARTLY_CLOUDLY_AND_RAIN, OVERCAST_AND_RAIN,
                       OVERCAST_THUNDERSTROMS_WITH_RAIN, CLOUDLY_AND_LIGHT_RAIN, OVERCAST_AND_LIGHT_RAIN,
                       CLOUDLY_AND_RAIN}

    SNOWY_CONDITIONS = {OVERCAST_AND_WET_SNOW, PARTLY_CLOUDLY_AND_LIGHT_SNOW, PARTLY_CLOUDLY_AND_SNOW,
                        OVERCAST_AND_SNOW, CLOUDLY_AND_LIGHT_SNOW, OVERCAST_AND_LIGHT_SNOW, CLOUDLY_AND_SNOW}


class Season(Enum):
    """
    The time of year in this locality.
    https://yandex.ru/dev/weather/doc/dg/concepts/forecast-test-docpage/
    """
    SUMMER = "summer"
    AUTUMN = "autumn"
    winter = "winter"
    spring = "spring"


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
