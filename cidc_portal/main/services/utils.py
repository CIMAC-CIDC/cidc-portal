from constants import URL_PREFIX


def url_for_with_prefix(url: str):
    """
    If we are serving the application under an existing URL path, we can
    use this to append a prefix to the URLs.

    Set PORTAL_URL_PREFIX in the environment, empty string for local development.
    :param url:
    :return:
    """
    return "%s%s" % (URL_PREFIX, url)
