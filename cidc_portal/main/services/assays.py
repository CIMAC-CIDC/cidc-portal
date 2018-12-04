from cidc_utils.requests import SmartFetch

from constants import EVE_URL

EVE_FETCHER = SmartFetch(EVE_URL)


def fetch_assays(jwt: str) -> dict:
    """
    Fetch all available assays in the system.

    Arguments:
        jwt {str} -- Requestor's JWT

    Returns:
        dict -- Assay records.
    """
    users_response = EVE_FETCHER.get(token=jwt, endpoint="assays")
    user_list = users_response.json()["_items"]

    return user_list
