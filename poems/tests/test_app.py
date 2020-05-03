import pytest

from poems import create_app, init_db

test_data = [
    {
        "type": "type1",
        "text": "poem of type1 number 1",
        "info": "info of type1 number 1",
    },
    {
        "type": "type1",
        "text": "poem of type1 number 2",
        "info": "info of type1 number 2",
    },
    {
        "type": "type2",
        "text": "poem of type2 number 1",
        "info": "info of type2 number 1",
    },
    {
        "type": "type2",
        "text": "poem of type2 number 2",
        "info": "info of type2 number 2",
    }
]


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        init_db(test_data)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_getting_poem(client):
    poem_data = client.get("/?weather=type1").json
    assert poem_data["text"] in [test_data[0]["text"],
                                 test_data[1]["text"]]
    assert poem_data["info"] in [test_data[0]["info"],
                                 test_data[1]["info"]]


def test_poem_and_info_are_consistent(client):
    poem_data = client.get("/?weather=type2").json
    text = poem_data["text"].split(' ', 1)[-1]
    info = poem_data["info"].split(' ', 1)[-1]
    assert text == info


def test_poem_not_found(client):
    response = client.get("/?weather=unknown")
    assert response.status_code == 404
