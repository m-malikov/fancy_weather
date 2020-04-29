import pytest
from flask import Flask

from generator import generate_picture

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

    def test_wrong_weather(self):
        with self.application.app_context():
            assert generate_picture('wrong_weather_type') is None

    def test_rainy(self):
        with self.application.app_context():
            pic_path = generate_picture('rainy')
            assert pic_path is not None
            assert 'rainy' in pic_path

    def test_snowy(self):
        with self.application.app_context():
            pic_path = generate_picture('snowy')
            assert pic_path is not None
            assert 'winter' in pic_path

    def test_cold(self):
        with self.application.app_context():
            pic_path = generate_picture('cold')
            assert pic_path is not None
            assert 'winter' in pic_path

    def test_warm(self):
        with self.application.app_context():
            pic_path = generate_picture('warm')
            assert pic_path is not None
            assert 'summer' in pic_path

    def test_spring(self):
        with self.application.app_context():
            pic_path = generate_picture('spring')
            assert pic_path is not None
            assert 'spring' in pic_path

    def test_autumn(self):
        with self.application.app_context():
            pic_path = generate_picture('autumn')
            assert pic_path is not None
            assert 'autumn' in pic_path
