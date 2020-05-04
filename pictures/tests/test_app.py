from flask import Flask

from pictures import generate_picture, init_available_images_collection

"""
Documentation: https://docs.pytest.org
Run all tests recursively in directories:
$ py.test
Run test group:
$ py.test -k TestMath
Useful flags: '-v' for verbose, '-l' for variables printing at error
"""


class TestPictureGenerator:
    def setup_class(self):
        self.application = Flask('pictures')
        self.images_links = init_available_images_collection(self.application)

    def test_wrong_weather(self):
        with self.application.app_context():
            assert generate_picture('wrong_weather_type',
                                    self.images_links) is None

    def test_rainy(self):
        with self.application.app_context():
            image_link = generate_picture('rainy', self.images_links)
            assert image_link is not None

    def test_snowy(self):
        with self.application.app_context():
            image_link = generate_picture('snowy', self.images_links)
            assert image_link is not None

    def test_cold(self):
        with self.application.app_context():
            image_link = generate_picture('cold', self.images_links)
            assert image_link is not None

    def test_warm(self):
        with self.application.app_context():
            image_link = generate_picture('warm', self.images_links)
            assert image_link is not None

    def test_spring(self):
        with self.application.app_context():
            image_link = generate_picture('spring', self.images_links)
            assert image_link is not None

    def test_autumn(self):
        with self.application.app_context():
            image_link = generate_picture('autumn', self.images_links)
            assert image_link is not None
