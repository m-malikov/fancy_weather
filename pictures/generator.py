import os
from enum import Enum
from random import choice
from typing import Optional

from flask import current_app


class Weather(Enum):
    RAINY = 'rainy'
    SNOWY = 'winter'
    COLD = 'winter'
    WARM = 'summer'
    SPRING = 'spring'
    AUTUMN = 'autumn'


def generate_picture(weather: str) -> Optional[str]:
    try:
        dir_name = Weather[weather.upper()].value
    except KeyError:
        return None

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'pic_storage/{dir_name}')

    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    current_app.logger.debug(f'Found {len(files)} files')

    return choice(files)


if __name__ == '__main__':
    print(generate_picture('rainy'))
