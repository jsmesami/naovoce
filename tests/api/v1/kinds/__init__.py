def kind_to_data(kind):
    return {
        "key": kind.key,
        "name": kind.name,
        "col": kind.color,
        "cls": kind.cls_name,
    }
