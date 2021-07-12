import pytest


@pytest.fixture
def signup_email_request_data(random_email, random_username, random_password):
    def closure(**kwargs):
        return {
            "email": kwargs.pop("email", random_email()),
            "username": kwargs.pop("username", random_username()),
            "password": kwargs.pop("password", random_password()),
        }

    return closure
