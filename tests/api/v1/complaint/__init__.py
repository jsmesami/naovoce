from fruit.models import Comment

TEXT_MAX_LENGTH = Comment._meta.get_field("text").max_length

BAD_COMPLAINT_CREATE_ARGS = [
    ({"foo": "bar"}, {"text": ["This field is required."]}),
    ({"text": None}, {"text": ["This field may not be null."]}),
    ({"text": ""}, {"text": ["This field may not be blank."]}),
    (
        {"text": "x" * (TEXT_MAX_LENGTH + 1)},
        {"text": ["Ensure this field has no more than {} characters.".format(TEXT_MAX_LENGTH)]},
    ),
]

REQUEST_DATA = {
    "text": "complaint",
}
