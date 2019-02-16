from . import format_coord, format_time, render_view_url, get_full_url


def fruit_to_data(fruit, response):
    return {
        'id': fruit.id,
        'lat': format_coord(fruit.position.y),
        'lng': format_coord(fruit.position.x),
        'kind': fruit.kind.key,
        'time': format_time(fruit.created),
        'url': render_view_url(response, 'api:fruit-detail', fruit.id),
     }


def fruit_to_verbose_data(fruit, response):
    return {
        'id': fruit.id,
        'lat': format_coord(fruit.position.y),
        'lng': format_coord(fruit.position.x),
        'kind': fruit.kind.key,
        'time': format_time(fruit.created),
        'url': render_view_url(response, 'api:fruit-detail', fruit.id),
        'description': fruit.description,
        'user': {
            'id': fruit.user.id,
            'username': fruit.user.username,
            'url': render_view_url(response, 'api:users-detail', fruit.user.id),
        },
        'images_count': 0,
        'images': render_view_url(response, 'api:image-list', fruit.id),
    }


def kind_to_data(kind):
    return {
        'key': kind.key,
        'name': kind.name,
        'col': kind.color,
        'cls': kind.cls_name,
    }


def user_to_data(user, response):
    return {
        'id': user.id,
        'username': user.username,
        'url': render_view_url(response, 'api:users-detail', user.id),
    }


def top_user_to_data(user, response):
    return {
        **user_to_data(user, response),
        'fruit_count': user.fruits.count(),
        'avatar': user.get_avatar(response.renderer_context['request']),
    }


def user_detail_to_data(user, response):
    return {
        **top_user_to_data(user, response),
        'fruit': render_view_url(response, 'api:fruit-list') + '?user={}'.format(user.id),
        'active': user.is_active,
        'motto': user.motto,
        'url': render_view_url(response, 'api:users-detail', user.id),
    }


def image_to_data(image, response):
    return {
        'id': image.id,
        'image': get_full_url(response, image.image.url),
        'caption': image.caption,
        'author': user_to_data(image.author, response),
    }


def season_to_data(season):
    return {
        'part': season.part,
        'start': season.start,
        'duration': season.duration,
    }


def herbarium_item_to_data(item):
    return {
        'name': item.name,
        'latin_name': item.latin_name,
        'description': item.description,
        'kind_key': item.kind.key,
        'seasons': list(map(season_to_data, item.seasons.all())),
    }
