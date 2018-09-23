import pytest

from teachtime.models import User

def test_user_model(session):
	user = User(
		username='username', 
		email='username@example.com', 
		password='password'
	)

	session.add(user)
	session.commit()

	assert user.id > 0