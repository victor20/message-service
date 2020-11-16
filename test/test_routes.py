import os
os.environ['DATABASE_URL'] = 'sqlite:///../test.db'

from messageservice import app, db
import pytest


@pytest.fixture
def client():
    db.drop_all()
    db.create_all()
    with app.test_client() as client:
        yield client


def test_1(client):

    # Add Users
    j = {"user_name": "Erik", "first_name": "Erik", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)
    assert 201 == rv.status_code
    assert b'{"message":"User successfully created"}\n' == rv.data

    # Username already in use
    rv = client.post('/api/users', json=j)
    assert 409 == rv.status_code
    assert b'Error username already in use' in rv.data

    # Missing data
    j = {"first_name": "Erik", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)
    assert 400 == rv.status_code
    assert b'Missing data for required field.' in rv.data

    # Get user
    rv = client.get('/api/users')
    assert 200 == rv.status_code
    users = rv.json['users']
    assert 1 == len(users)
    assert "Erik" == users[0]['user_name']
    assert "Erik" == users[0]['first_name']
    assert "Pregen" == users[0]['last_name']

def test_2(client):

    # Add users
    j = {"user_name": "Carl", "first_name": "Carl", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)
    j = {"user_name": "Victor", "first_name": "Victor", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)
    j = {"user_name": "Douglas", "first_name": "Douglas", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)

    # Add messages
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Carl/messages', json=j)
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Carl/messages', json=j)
    assert 201 == rv.status_code
    assert b'{"message":"Message successfully sent"}\n' == rv.data

    # Wrong url/sender
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/xxxx/messages', json=j)
    assert 404 == rv.status_code
    assert b'User not found' in rv.data

    # Wrong reciver
    j = {"receiver": "xxxx", "message_text": "Hej Fredrik"}
    rv = client.post('/api/users/Victor/messages', json=j)
    assert 400 == rv.status_code
    assert b'Receiver not found' in rv.data

    # Missing data
    j = {"message_text": "Hej Fredrik"}
    rv = client.post('/api/users/Carl/messages', json=j)
    assert 400 == rv.status_code
    assert b'Missing data for required field.' in rv.data

    # Get message
    rv = client.get('/api/messages')
    assert 200 == rv.status_code
    messages = rv.json['messages']
    assert 2 == len(messages)
    assert "Carl" == messages[1]['sender']
    assert "Victor" == messages[1]['receiver']
    assert "Hej Victor" == messages[1]['message_text']

def test_3(client):

    # Add users
    j = {"user_name": "Carl", "first_name": "Carl", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)
    j = {"user_name": "Victor", "first_name": "Victor", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)
    j = {"user_name": "Douglas", "first_name": "Douglas", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)

    # Add messages
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Carl/messages', json=j)
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Carl/messages', json=j)
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Douglas/messages', json=j)

    # Wrong user
    rv = client.get('/api/users/xxxx/messages/received?from=1&to=2')
    assert 404 == rv.status_code
    assert b'User not found' in rv.data

    # Wrong index 1
    rv = client.get('/api/users/Victor/messages/received?from=0&to=2')
    assert 400 == rv.status_code
    assert b'Must be greater than or equal to 1' in rv.data

    # Wrong index 2
    rv = client.get('/api/users/Victor/messages/received?from=-20&to=2')
    assert 400 == rv.status_code
    assert b'Must be greater than or equal to 1' in rv.data

    # Wrong index 3
    rv = client.get('/api/users/Victor/messages/received?from=300&to=2')
    assert 400 == rv.status_code
    assert b'from_index must be greater than to_index' in rv.data

    # Non integer
    rv = client.get('/api/users/Victor/messages/received?from=x&to=2')
    assert 400 == rv.status_code
    assert b'Not a valid integer.' in rv.data

    # Text index
    rv = client.get('/api/users/Victor/messages/received?from=1&to=2')
    assert 200 == rv.status_code
    messages = rv.json['messages']
    assert 1 == len(messages)

    # Text index
    rv = client.get('/api/users/Victor/messages/received?from=1&to=1')
    assert 200 == rv.status_code
    messages = rv.json['messages']
    assert 0 == len(messages)

    # Get message
    rv = client.get('/api/users/Victor/messages/received?from=1&to=4')
    assert 200 == rv.status_code
    messages = rv.json['messages']
    assert 3 == len(messages)
    assert "Carl" == messages[0]['sender']
    assert "Victor" == messages[0]['receiver']
    assert "Hej Victor" == messages[0]['message_text']

def test_4(client):

    # Add users
    j = {"user_name": "Carl", "first_name": "Carl", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)
    j = {"user_name": "Victor", "first_name": "Victor", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)

    # Add messages
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Carl/messages', json=j)
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Carl/messages', json=j)

    # Wrong user
    rv = client.get('/api/users/xxxx/messages/received/new')
    assert 404 == rv.status_code
    assert b'User not found' in rv.data

    # Test new with unread messages
    rv = client.get('/api/users/Victor/messages/received/new')
    assert 200 == rv.status_code
    messages = rv.json['messages']
    assert 2 == len(messages)
    assert "Carl" == messages[0]['sender']
    assert "Victor" == messages[0]['receiver']
    assert "Hej Victor" == messages[0]['message_text']

    # Test new with read messages
    rv = client.get('/api/users/Victor/messages/received/new')
    assert 200 == rv.status_code
    messages = rv.json['messages']
    assert 0 == len(messages)

def test_5(client):

    # Add users
    j = {"user_name": "Carl", "first_name": "Carl", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)
    j = {"user_name": "Victor", "first_name": "Victor", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)
    j = {"user_name": "Douglas", "first_name": "Douglas", "last_name": "Pregen"}
    rv = client.post('/api/users', json=j)

    # Add messages
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Carl/messages', json=j)
    j = {"receiver": "Carl", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Victor/messages', json=j)
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Carl/messages', json=j)
    j = {"receiver": "Victor", "message_text": "Hej Victor"}
    rv = client.post('/api/users/Douglas/messages', json=j)

    # Wrong user
    rv = client.delete('/api/users/xxxx/messages')
    assert 404 == rv.status_code
    assert b'User not found' in rv.data

    # Non integer
    j = {"messages": [1, 'xxx', 2]}
    rv = client.delete('/api/users/Victor/messages', json=j)
    assert 400 == rv.status_code
    assert b'Not a valid integer.' in rv.data

    # Delete messages
    j = {"messages": [1, 2]}
    rv = client.delete('/api/users/Victor/messages', json=j)
    assert 204 == rv.status_code

    # Get user messages
    rv = client.get('/api/users/Victor/messages/received?from=1&to=5')
    assert 200 == rv.status_code
    messages = rv.json['messages']
    assert 2 == len(messages)

    # Get all messages
    rv = client.get('/api/messages')
    assert 200 == rv.status_code
    messages = rv.json['messages']
    assert 3 == len(messages)
    assert "Carl" == messages[1]['sender']
    assert "Victor" == messages[1]['receiver']
    assert "Hej Victor" == messages[1]['message_text']
