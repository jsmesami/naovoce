from user import constants

TOKEN_BAD_ARGS = [
    (
        {"email": "e" * (constants.EMAIL_MAX_LENGTH + 1)},
        {
            "email": [
                f"Ensure this field has no more than {constants.EMAIL_MAX_LENGTH} characters.",
                "Enter a valid email address.",
            ]
        },
    ),
    ({"email": None}, {"email": ["This field may not be null."]}),
    ({"email": ""}, {"email": ["This field may not be blank."]}),
    (
        {"fcb_id": "i" * (constants.FCB_ID_MAX_LENGTH + 1)},
        {"fcb_id": [f"Ensure this field has no more than {constants.FCB_ID_MAX_LENGTH} characters."]},
    ),
    ({"fcb_id": None}, {"fcb_id": ["This field may not be null."]}),
    ({"fcb_id": ""}, {"fcb_id": ["This field may not be blank."]}),
]

SIGNUP_BAD_ARGS = TOKEN_BAD_ARGS + [
    (
        {"fcb_token": "t" * (constants.FCB_TOKEN_MAX_LENGTH + 1)},
        {"fcb_token": [f"Ensure this field has no more than {constants.FCB_TOKEN_MAX_LENGTH} characters."]},
    ),
    ({"fcb_token": None}, {"fcb_token": ["This field may not be null."]}),
    ({"fcb_token": ""}, {"fcb_token": ["This field may not be blank."]}),
]
