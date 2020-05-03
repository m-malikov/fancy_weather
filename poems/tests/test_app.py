import pytest
import os
import tempfile
import json

from poems import poems
from poems.poem_finder import PoemFinder

test_data = {
    "type1": [
        {
            "text": "poem of type1 number 1",
            "info": "info of type1 number 1",
        },
        {
            "text": "poem of type1 number 2",
            "info": "info of type1 number 2",
        }
    ],
    "type2": [
        {
            "text": "poem of type2 number 1",
            "info": "info of type2 number 1",
        },
        {
            "text": "poem of type2 number 2",
            "info": "info of type2 number 2",
        }
    ]
}


@pytest.fixture
def client():
    poems_fd, poems_filename = tempfile.mkstemp()
    poems.app.config["TESTING"] = True
    os.write(poems_fd, json.dumps(test_data).encode("utf-8"))

    with poems.app.test_client() as client:
        with poems.app.app_context():
            poems.poem_finder = PoemFinder(poems_filename)
        yield client

    os.close(poems_fd)
    os.unlink(poems_filename)


def test_getting_poem(client):
    poem_data = client.get("/?weather=type1").json
    assert poem_data["text"] in [test_data["type1"][0]["text"],
                                 test_data["type1"][1]["text"]]
    assert poem_data["info"] in [test_data["type1"][0]["info"],
                                 test_data["type1"][1]["info"]]


def test_poem_and_info_are_consistent(client):
    poem_data = client.get("/?weather=type2").json
    text = poem_data["text"][5:]
    info = poem_data["info"][5:]
    assert text == info


def test_poem_not_found(client):
    response = client.get("/?weather=unknown")
    assert response.status_code == 404
