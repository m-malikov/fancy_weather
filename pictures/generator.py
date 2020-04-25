import os
from enum import Enum
from random import choice
from typing import Optional


class Weather(Enum):
    rainy = 'rainy'
    snowy = 'winter'
    cold = 'winter'
    warm = 'summer'
    spring = 'spring'
    autumn = 'autumn'


def generate_picture(weather: str) -> Optional[str]:
    try:
        dir_name = Weather[weather].value
    except KeyError:
        return None

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic_storage/' + dir_name)

    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    return choice(files)


if __name__ == '__main__':
    print(generate_picture('rainy'))
