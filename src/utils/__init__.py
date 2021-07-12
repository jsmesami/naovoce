import mimetypes


def trim_words(s, max_chars, separator=" "):
    """Trim sentence at last word preceding max_chars."""

    if max_chars and len(s) >= max_chars:
        head, sep, tail = s[:max_chars].rpartition(separator)
        return (head or tail) + "..."

    return s


# This is here because mimetypes.guess_extension() sometimes returns odd results.
MIMETYPE_TO_EXTENSION = {
    "image/jpeg": "JPEG",
    "image/png": "PNG",
    "image/gif": "GIF",
}


def guess_extension(mimetype):
    ext = mimetypes.guess_extension(mimetype)
    if ext is None:
        return "Unknown"

    return ext[1:].upper()


def extension_for_mimetype(mimetype):
    return MIMETYPE_TO_EXTENSION.get(mimetype) or guess_extension(mimetype)
