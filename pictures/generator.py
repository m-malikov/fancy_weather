from enum import Enum
from random import choice
from typing import Dict, List, Optional


class WeatherToImgurAlbum(Enum):
    RAINY = 'hD9TtOi'
    SNOWY = '1OYnx6T'
    COLD = '1OYnx6T'
    WARM = 'ZFHVUYq'
    SPRING = 'e2NdXQn'
    AUTUMN = 'Qp8PziJ'


def generate_picture(weather: str, images_links: Dict[str, List[str]]) -> Optional[str]:
    try:
        imgur_album = WeatherToImgurAlbum[weather.upper()].value
    except KeyError:
        return None

    links_for_album = images_links[imgur_album]
    return choice(links_for_album)
