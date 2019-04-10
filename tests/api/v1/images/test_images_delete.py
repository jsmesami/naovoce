from rest_framework import status
from rest_framework.reverse import reverse


def test_image_delete(client, random_password, new_user, new_image):
    password = random_password()
    user = new_user(password=password)
    image = new_image(author=user)

    assert client.login(username=user.username, password=password)

    response = client.delete(reverse('api:image-detail', args=[image.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_image_delete_unauthenticated(client, random_password, new_user, new_image):
    user = new_user()
    image = new_image(author=user)

    response = client.delete(reverse('api:image-detail', args=[image.id]))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_image_delete_unauthorized(client, random_password, new_user, new_image):
    image = new_image()
    password = random_password()
    different_user = new_user(password=password)

    assert client.login(username=different_user.username, password=password)

    response = client.delete(reverse('api:image-detail', args=[image.id]))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'You do not have permission to perform this action.'}
