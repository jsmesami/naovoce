import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from fruit.models import Fruit, Comment

TEXT_MAX_LENGTH = Comment._meta.get_field('text').max_length
BAD_COMPLAINT_CREATE_ARGS = [
    ({'foo': 'bar'},
     {'text': ['This field is required.']}),
    ({'text': None},
     {'text': ['This field may not be null.']}),
    ({'text': ''},
     {'text': ['This field may not be blank.']}),
    ({'text': 'x' * (TEXT_MAX_LENGTH + 1)},
     {'text': ['Ensure this field has no more than {} characters.'.format(TEXT_MAX_LENGTH)]}),
]
REQUEST_DATA = {
    'text': 'complaint',
}


def test_complaint(client, truncate_table, random_password, new_user, new_fruit):
    truncate_table(Comment)
    password = random_password()
    user = new_user(password=password)
    fruit = new_fruit()

    assert client.login(username=user.username, password=password)

    response = client.post(
        reverse('api:fruit-complaint', args=[fruit.id]),
        REQUEST_DATA,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert REQUEST_DATA == response.json()

    comment = Comment.objects.last()

    assert comment.fruit_id == fruit.id
    assert comment.author_id == user.id
    assert comment.text == REQUEST_DATA['text']
    assert comment.is_complaint is True


@pytest.mark.django_db
def test_complaint_nonexistent_fruit(client, truncate_table, random_password, new_user):
    truncate_table(Fruit)
    password = random_password()
    user = new_user(password=password)

    assert client.login(username=user.username, password=password)

    response = client.post(
        reverse('api:fruit-complaint', args=[1]),
        REQUEST_DATA,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Not found.'}


def test_complaint_unauthorized(client, new_fruit):
    fruit = new_fruit()

    response = client.post(
        reverse('api:fruit-complaint', args=[fruit.id]),
        REQUEST_DATA,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


@pytest.mark.parametrize('bad_args, error_msg', BAD_COMPLAINT_CREATE_ARGS)
def test_complaint_bad_args(client, random_password, new_user, new_fruit, bad_args, error_msg):
    password = random_password()
    user = new_user(password=password)
    fruit = new_fruit()

    assert client.login(username=user.username, password=password)

    response = client.post(
        reverse('api:fruit-complaint', args=[fruit.id]),
        bad_args,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error_msg
