from django.conf import settings

from user import constants

SIGNUP_BAD_ARGS = [
    ({"username": None}, {"username": ["This field may not be null."]}),
    ({"username": ""}, {"username": ["This field may not be blank."]}),
    ({"username": "user\x00name"}, {"username": ["Null characters are not allowed."]}),
    (
        {"username": "u" * (constants.USERNAME_MAX_LENGTH + 1)},
        {"username": [f"Ensure this field has no more than {constants.USERNAME_MAX_LENGTH} characters."]},
    ),
    ({"email": None}, {"email": ["This field may not be null."]}),
    ({"email": ""}, {"email": ["This field may not be blank."]}),
    ({"email": "invalid"}, {"email": ["Enter a valid email address."]}),
    ({"email": "invalid@"}, {"email": ["Enter a valid email address."]}),
    ({"email": "invalid@domain"}, {"email": ["Enter a valid email address."]}),
    ({"email": "@domain.com"}, {"email": ["Enter a valid email address."]}),
    ({"password": None}, {"password": ["This field may not be null."]}),
    ({"password": ""}, {"password": ["This field may not be blank."]}),
    (
        {"password": "abc"},
        {"password": [f"Ensure this field has at least {settings.PASSWORD_MIN_LENGTH} characters."]},
    ),
]
