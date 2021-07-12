from ..utils import format_coord, format_time, render_view_url

BAD_FRUIT_CRUD_ARGS = [
    ({"kind": None}, {"kind": ["This field may not be null."]}),
    ({"kind": ""}, {"kind": ["This field may not be null."]}),
    ({"kind": "nonexistent"}, {"kind": ["nonexistent is not a valid Kind key."]}),
    ({"lat": None}, {"lat": ["This field may not be null."]}),
    ({"lat": ""}, {"lat": ["A valid number is required."]}),
    ({"lat": "NaN"}, {"lat": ["A valid number is required."]}),
    (
        {"lat": "60.1234564567890"},
        {"lat": ["Ensure that there are no more than 13 digits in total."]},
    ),
    ({"lng": None}, {"lng": ["This field may not be null."]}),
    ({"lng": ""}, {"lng": ["A valid number is required."]}),
    ({"lng": "NaN"}, {"lng": ["A valid number is required."]}),
    (
        {"lng": "60.1234564567890"},
        {"lng": ["Ensure that there are no more than 13 digits in total."]},
    ),
]


def fruit_to_data(fruit, response):
    return {
        "id": fruit.id,
        "lat": format_coord(fruit.position.y),
        "lng": format_coord(fruit.position.x),
        "kind": fruit.kind.key,
        "time": format_time(fruit.created),
        "url": render_view_url(response, "api:fruit-detail", fruit.id),
    }


def fruit_to_verbose_data(fruit, response):
    return {
        "id": fruit.id,
        "lat": format_coord(fruit.position.y),
        "lng": format_coord(fruit.position.x),
        "kind": fruit.kind.key,
        "time": format_time(fruit.created),
        "url": render_view_url(response, "api:fruit-detail", fruit.id),
        "description": fruit.description,
        "user": {
            "id": fruit.user.id,
            "username": fruit.user.username,
            "url": render_view_url(response, "api:users-detail", fruit.user.id),
        },
        "images_count": 0,
        "images": render_view_url(response, "api:image-list", fruit.id),
    }
