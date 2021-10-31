
from CICDPractice2.app import app


def test_get_page():
    app.config['TESTING'] = True
    client = app.test_client()

    result = client.get('/')
    assert b'Hello World' in result.data

def test_get_bar():
    app.config['TESTING'] = True
    client = app.test_client()

    result = client.get('/foo?bar=1000000')
    assert b'1000000' in result.data

def test_get_foobar():
    app.config['TESTING'] = True
    client = app.test_client()

    result = client.get('/bar')
    assert b'Bar' in result.data
