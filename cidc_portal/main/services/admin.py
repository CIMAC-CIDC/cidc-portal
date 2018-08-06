import json

from cidc_utils.requests import SmartFetch

from constants import EVE_URL
EVE_FETCHER = SmartFetch(EVE_URL)


def fetch_users(jwt):

    users_response = EVE_FETCHER.get(token=jwt, endpoint='accounts')

    user_list = users_response.json()["_items"]

    return user_list


def fetch_trials(jwt):
    trials_response = EVE_FETCHER.get(token=jwt, endpoint='trials')
    trials_list = trials_response.json()["_items"]

    return trials_list


def fetch_single_user(jwt, selected_user):

    endpoint_with_query = "accounts/%s" % selected_user
    users_response = EVE_FETCHER.get(token=jwt, endpoint=endpoint_with_query)

    return users_response.json()


def fetch_users_trials(jwt, selected_user):
    trial_params = {'collaborators': selected_user}
    endpoint_with_query = "trials?where=%s" % (json.dumps(trial_params))
    trials_response = EVE_FETCHER.get(token=jwt, endpoint=endpoint_with_query)
    return trials_response.json()["_items"]
