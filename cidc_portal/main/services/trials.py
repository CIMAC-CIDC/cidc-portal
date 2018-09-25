from cidc_utils.requests import SmartFetch

from constants import EVE_URL

EVE_FETCHER = SmartFetch(EVE_URL)


def fetch_trials(jwt: str) -> dict:
    """
    Get all the trials in the system.

    :param jwt: Users JWT
    :return: Dict of all trials in system.
    """
    trials_response = EVE_FETCHER.get(token=jwt, endpoint="trials")
    trials_list = trials_response.json()["_items"]

    return trials_list
