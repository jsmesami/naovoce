import facebook
import pytest

from user.models import FacebookInfo

FCB_ID = "110045436843169"

FCB_TOKEN = (
    "EAADvcY7nZCq8BAGbU0JMgZCaOPtQZBZBuioYJcIghkoFu2A26HWWzykYhcnVYY6ihNZBVh"
    "QlHFpnMeZBAhpobEA6bGTLbPw3Fqbfsv8SfgsP2augzlcWFcZCe2uDDs9DP6f3PNZBZAM0c"
    "OnwxdhzRorxugOfO1EHJuyw2jhcQMZCzJVCfhq8FWpb40CmFPwg1WNQbtktW11hOiggZDZD"
)


@pytest.fixture
def signup_facebook_request_data(random_email):
    def closure(**kwargs):
        return {
            "email": kwargs.pop("email", random_email()),
            "fcb_id": kwargs.pop("fcb_id", FCB_ID),
            "fcb_token": kwargs.pop("fcb_token", FCB_ID),
        }

    return closure


@pytest.fixture
@pytest.mark.django_db
def new_facebook_info(new_user):
    def closure(**kwargs):
        return FacebookInfo.objects.create(
            user=kwargs.pop("user", None) or new_user(),
            fcb_id=kwargs.pop("fcb_id", FCB_ID),
            fcb_token=kwargs.pop("fcb_token", FCB_TOKEN),
            **kwargs
        )

    return closure


@pytest.fixture
def mock_facebook(monkeypatch):
    def closure(fails=False, **overrides):
        def get_object(*args, **kwargs):
            if fails:
                raise facebook.GraphAPIError("Facebook error")

            return {
                "first_name": overrides.pop("first_name", "Isaac"),
                "last_name": overrides.pop("last_name", "Asimov"),
                "id": overrides.pop("fcb_id", FCB_ID),
                "picture": {
                    "data": {
                        "height": 200,
                        "is_silhouette": True,
                        "url": "https://platform-lookaside.fbsbx.com/platform/profilepic/"
                        "?asid=110045436843169"
                        "&height=200"
                        "&width=200"
                        "&ext=1556829832"
                        "&hash=AeSLD93lbSjc5t96",
                        "width": 200,
                    },
                },
            }

        monkeypatch.setattr(facebook.GraphAPI, "get_object", get_object)

    return closure
