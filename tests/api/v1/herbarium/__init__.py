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
