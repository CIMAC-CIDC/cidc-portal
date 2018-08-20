import json

from cidc_utils.requests import SmartFetch

from constants import EVE_URL
EVE_FETCHER = SmartFetch(EVE_URL)


def fetch_users(jwt: str) -> dict:
    """
    Get all the users in the system.

    :param jwt: Users JWT
    :return: Dict of all users in system.
    """
    users_response = EVE_FETCHER.get(token=jwt, endpoint='accounts')
    user_list = users_response.json()["_items"]

    return user_list


def fetch_single_user(jwt: str, selected_user: str) -> dict:
    """
    Get accounts object for a single user.

    :param jwt: Admin Users JWT
    :param selected_user: Username of the user you wish to retrieve data on.
    :return:
    """
    endpoint_with_query = "accounts/%s" % selected_user
    users_response = EVE_FETCHER.get(token=jwt, endpoint=endpoint_with_query)

    return users_response.json()


def fetch_users_trials(jwt: str, selected_user: str) -> dict:
    """
    Get all the trials a given user is collaborator on.
    
    :param jwt: Admin Users JWT
    :param selected_user: Username of the user whose trials you want to retrieve
    :return:
    """

    trial_params = {'collaborators': selected_user}
    endpoint_with_query = "trials?where=%s" % (json.dumps(trial_params))
    trials_response = EVE_FETCHER.get(token=jwt, endpoint=endpoint_with_query)

    return trials_response.json()["_items"]
