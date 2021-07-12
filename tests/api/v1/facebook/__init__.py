from user import constants

TOKEN_BAD_ARGS = [
    (
        {"email": "e" * (constants.EMAIL_MAX_LENGTH + 1)},
        {
            "email": [
                "Ensure this field has no more than {} characters.".format(constants.EMAIL_MAX_LENGTH),
                "Enter a valid email address.",
            ]
        },
    ),
    ({"email": None}, {"email": ["This field may not be null."]}),
    ({"email": ""}, {"email": ["This field may not be blank."]}),
    (
        {"fcb_id": "i" * (constants.FCB_ID_MAX_LENGTH + 1)},
        {"fcb_id": ["Ensure this field has no more than {} characters.".format(constants.FCB_ID_MAX_LENGTH)]},
    ),
    ({"fcb_id": None}, {"fcb_id": ["This field may not be null."]}),
    ({"fcb_id": ""}, {"fcb_id": ["This field may not be blank."]}),
]

SIGNUP_BAD_ARGS = TOKEN_BAD_ARGS + [
    (
        {"fcb_token": "t" * (constants.FCB_TOKEN_MAX_LENGTH + 1)},
        {"fcb_token": ["Ensure this field has no more than {} characters.".format(constants.FCB_TOKEN_MAX_LENGTH)]},
    ),
    ({"fcb_token": None}, {"fcb_token": ["This field may not be null."]}),
    ({"fcb_token": ""}, {"fcb_token": ["This field may not be blank."]}),
]
