from contextlib import suppress

with suppress(ImportError):
    from .local import *  # noqa:F401,F403
