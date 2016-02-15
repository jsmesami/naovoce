import locale
from operator import itemgetter, attrgetter


def naturalsort(iterable, key=None):
    """
    Locale-aware alphabetical string sorting,
    Besides string, key can be index or argument name
    """
    locale.setlocale(locale.LC_ALL, '')

    _getter = itemgetter(key) if isinstance(key, int) else attrgetter(key) if key else str

    # unicode collation doesn't work on development box with OSX for some reason.
    return sorted(iterable, key=lambda obj: locale.strxfrm(_getter(obj)))


def trim_words(s, max_chars, separator=' '):
    """
    Trim sentence at last word preceding max_chars
    """
    if max_chars and len(s) >= max_chars:
        head, sep, tail = s[:max_chars].rpartition(separator)
        return (head or tail)+'...'
    else:
        return s
