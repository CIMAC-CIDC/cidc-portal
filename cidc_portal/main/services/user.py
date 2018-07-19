from constants import EVE_URL

from cidc_utils.requests import SmartFetch

EVE_FETCHER = SmartFetch(EVE_URL)


def get_user_role(jwt):
    try:
        trials_response = EVE_FETCHER.get(token=jwt, endpoint='accounts', verify=False)
        return trials_response.json()['_items']
    except RuntimeError:
        return ["CIMAC_BIOFX"]


def get_trials(jwt):
    try:
        trials_response = EVE_FETCHER.get(token=jwt, endpoint='trials', verify=False)
        return trials_response.json()['_items']
    except RuntimeError:
        return []


def get_cimac_biofox_user_home_data(jwt):
    user_info = {}

    user_info["registration_status"] = None
    user_info["code_of_coduct_status"] = None
    user_info["gcp_upload_permission"] = None
    user_info["trials"] = None

    user_info["trials"] = get_trials(jwt)

    return user_info





