from user import constants

TOKEN_BAD_ARGS = [
    (
        {"username": "u" * (constants.USERNAME_MAX_LENGTH + 1)},
        {"non_field_errors": ["Unable to log in with provided credentials."]},
    ),
    ({"username": None}, {"username": ["This field may not be null."]}),
    ({"username": ""}, {"username": ["This field may not be blank."]}),
    (
        {"password": "bad_password"},
        {"non_field_errors": ["Unable to log in with provided credentials."]},
    ),
    (
        {"password": "p" * (constants.PASSWORD_MAX_LENGTH + 1)},
        {"non_field_errors": ["Unable to log in with provided credentials."]},
    ),
    ({"password": None}, {"password": ["This field may not be null."]}),
    ({"password": ""}, {"password": ["This field may not be blank."]}),
]
