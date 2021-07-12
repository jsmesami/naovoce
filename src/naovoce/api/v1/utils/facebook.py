import facebook
from funcy import get_in

from user import constants
from user.models import FacebookInfo, FruitUser


def verify_user(fcb_id, fcb_token):
    return facebook.GraphAPI(access_token=fcb_token).get_object(
        id=fcb_id,
        fields="first_name, last_name, picture.type(large)",
    )


def get_picture_url(fcb_user):
    if get_in(fcb_user, ["picture", "data", "is_silhouette"]):
        return ""

    return get_in(fcb_user, ["picture", "data", "url"], "")


def get_first_name(fcb_user):
    return fcb_user.get("first_name", "")[: constants.FIRST_NAME_MAX_LENGTH]


def get_last_name(fcb_user):
    return fcb_user.get("last_name", "")[: constants.LAST_NAME_MAX_LENGTH]


def generate_unique_username(fcb_user):
    nickname = get_first_name(fcb_user) or get_last_name(fcb_user) or "Picker"
    unique_username = nickname
    count = 1

    while True:
        if FruitUser.objects.filter(username=unique_username).exists():
            unique_username = nickname + str(count)
            count += 1
        else:
            return unique_username


def create_user(fcb_user, email, fcb_id, fcb_token):
    user = FruitUser.objects.create_user(
        username=generate_unique_username(fcb_user),
        first_name=get_first_name(fcb_user),
        last_name=get_last_name(fcb_user),
        email=email,
        is_email_verified=True,
    )

    user.set_unusable_password()
    user.save()

    FacebookInfo.objects.create(
        user=user,
        fcb_id=fcb_id,
        fcb_token=fcb_token,
        picture_url=get_picture_url(fcb_user),
        raw_data=fcb_user,
    )

    return user


def connect_user(fcb_user, user, fcb_id, fcb_token):
    user.is_email_verified = True

    if not user.first_name:
        user.first_name = get_first_name(fcb_user)

    if not user.last_name:
        user.last_name = get_last_name(fcb_user)

    user.save()

    info, _ = FacebookInfo.objects.update_or_create(
        user=user,
        defaults=dict(
            fcb_id=fcb_id,
            fcb_token=fcb_token,
            picture_url=get_picture_url(fcb_user),
            raw_data=fcb_user,
        ),
    )

    return user
