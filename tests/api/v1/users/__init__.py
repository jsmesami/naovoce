from ..utils import render_view_url


def user_to_data(user, response):
    return {
        "id": user.id,
        "username": user.username,
        "url": render_view_url(response, "api:users-detail", user.id),
    }


def top_user_to_data(user, response):
    return {
        **user_to_data(user, response),
        "fruit_count": user.fruits.count(),
        "avatar": user.get_avatar(response.renderer_context["request"]),
    }


def user_detail_to_data(user, response):
    return {
        **top_user_to_data(user, response),
        "fruit": render_view_url(response, "api:fruit-list") + f"?user={user.id}",
        "active": user.is_active,
        "motto": user.motto,
        "url": render_view_url(response, "api:users-detail", user.id),
    }
