"""
Collection of custom jinja2 filters for templating
"""

import os


def env_override(value, key):
    """
    Get the value of an environment variable or the default.

    From https://stackoverflow.com/a/25864212/379566

    :param value: the default value
    :param key: environment variable
    :rtype: str
    """
    return os.getenv(key, value)
