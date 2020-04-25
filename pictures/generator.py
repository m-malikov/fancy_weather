import os
from enum import Enum
from random import choice


class Weather(Enum):
    rainy = 'rainy'
    snowy = 'winter'
    cold = 'winter'
    warm = 'summer'
    spring = 'spring'
    autumn = 'autumn'


def generate_picture(weather: str):
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

    # source_image = cv2.imread('pic_storage/1506418628_aleksey-savrasov-grachi-prileteli.jpg')
    #
    # # Do some processing, get output_img
    #
    # _, buffer = cv2.imencode('.jpg', source_image)
    # return buffer.tobytes()


if __name__ == '__main__':
    print(generate_picture('rainy'))
