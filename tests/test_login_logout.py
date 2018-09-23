import pytest

def test_login_logout(test_user, client):
    response = pytest.helpers.login(client, 'username', 'username@example.com')
    assert '' in response

    response = pytest.helpers.logout(client)
    assert '' in response