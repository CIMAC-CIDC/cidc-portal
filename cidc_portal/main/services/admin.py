"""
Defines functions for administrators to manage users.
"""
import json
import logging
from typing import List
from flask import session
import deprecation

from cidc_utils.requests import SmartFetch


from constants import EVE_URL
from constants import ROLE_LIST

EVE_FETCHER = SmartFetch(EVE_URL)


def fetch_users(jwt: str) -> dict:
    """
    Get all the users in the system.

    :param jwt: Users JWT
    :return: Dict of all users in system.
    """
    users_response = EVE_FETCHER.get(token=jwt, endpoint="accounts")
    user_list = users_response.json()["_items"]

    return user_list


@deprecation.deprecated(details="Use the function user_fetch instead.")
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


def user_fetch(jwt: str, user_ids: List[str]) -> dict:
    """
    Fetch the accounts records for one or more users.

    Arguments:
        jwt {str} -- Requestor's JWT
        user_ids {List[str]} -- List of user IDs.

    Returns:
        dict -- Account records.
    """

    query = {"$in": user_ids}
    endpoint_with_query = 'accounts/?where={"_id":%s}' % (json.dumps(query))

    return EVE_FETCHER.get(token=jwt, endpoint=endpoint_with_query).json()


def fetch_users_trials(jwt: str, selected_user: str) -> dict:
    """
    Get all the trials a given user is collaborator on.

    :param jwt: Admin Users JWT
    :param selected_user: Username of the user whose trials you want to retrieve
    :return:
    """
    trial_params = {"collaborators": selected_user}
    endpoint_with_query = "trials?where=%s" % (json.dumps(trial_params))

    trials_response = EVE_FETCHER.get(token=jwt, endpoint=endpoint_with_query)

    return trials_response.json()


def add_user_to_trial(jwt: str, trial_id: str, user_ids: List[str]) -> bool:
    """
    Adds a user or users to a trial.

    Arguments:
        jwt {str} -- [description]
        trial_id {str} -- [description]
        user_ids {List[str]} -- [description]

    Returns:
        bool -- True if addition is successful, else false.
    """
    # Get users emails
    user_records = user_fetch(jwt, user_ids)["_items"]
    emails = [user["email"] for user in user_records]

    trial_query = "trials/%s" % trial_id
    trial_info = EVE_FETCHER.get(token=jwt, endpoint=trial_query).json()
    trial_etag = trial_info["_etag"]
    trial_collabs = trial_info["collaborators"]

    updated_collabs = set(emails + trial_collabs)

    if len(updated_collabs) == len(trial_collabs):
        logging.warning(
            {
                "message": "Warning! Updated collaborators list is identical to current list."
                "Operation not performed.",
                "category": "WARNING-PORTAL-FAIR-UPDATE-COLLABORATORS",
            }
        )
        return False

    payload = {"collaborators": list(updated_collabs)}

    try:
        EVE_FETCHER.post(
            json=payload,
            headers={"If-Match": trial_etag, "X-HTTP-Method-Override": "PATCH"},
            token=jwt,
            endpoint=trial_query,
        )

        logging.info({
                "message": "User(s) %s added to trial %s by %s" %
                           (emails, trial_id, session["cidc_user_info"]["username"]),
                "category": "INFO-PORTAL-ADD-USER-TRIAL"})

        return True
    except RuntimeError:
        return False


def remove_user_from_trial(jwt: str, trial_id: str, user_ids: List[str]) -> bool:
    """
    Removed a user from trial.

    Arguments:
        jwt {str} -- [description]
        trial_id {str} -- [description]
        user_ids {List[str]} -- [description]

    Returns:
        bool -- True if addition is successful, else false.
    """
    # Get users emails
    user_records = user_fetch(jwt, user_ids)["_items"]
    emails = [user["email"] for user in user_records]

    trial_query = "trials/%s" % trial_id
    trial_info = EVE_FETCHER.get(token=jwt, endpoint=trial_query).json()
    trial_collabs = trial_info["collaborators"]

    updated_collabs = set(trial_collabs) - set(emails)

    if len(updated_collabs) == len(trial_collabs):
        logging.warning(
            {
                "message": "Warning! No one was removed from collaborator list."
                "Operation not performed.",
                "category": "WARNING-PORTAL-FAIR-UPDATE-COLLABORATORS",
            }
        )
        return False

    payload = {"collaborators": list(updated_collabs)}

    try:
        EVE_FETCHER.post(
            json=payload,
            headers={
                "If-Match": trial_info["_etag"],
                "X-HTTP-Method-Override": "PATCH",
            },
            token=jwt,
            endpoint=trial_query,
        )

        logging.info({
                "message": "User(s) %s removed from trial %s by %s" %
                           (emails, trial_id, session["cidc_user_info"]["username"]),
                "category": "INFO-PORTAL-REMOVE-USER-TRIAL"})

        return True
    except RuntimeError:
        return False


def change_user_role(jwt: str, user_id: str, role: str) -> bool:
    """
    Changes the role of the designated user to the specified role.

    Arguments:
        jwt {str} -- [description]
        user_id {str} -- [description]
        role {str} -- [description]

    Returns:
        bool -- True if change works, else false.
    """
    #  Check if the role is a valid role.
    if role not in ROLE_LIST:
        log = "Supplied role % is not a valid role" % role
        logging.warning({"message": log, "category": "WARNING-PORTAL-ACCOUNTS"})
        return

    endpoint_with_query = "accounts/%s" % user_id
    user_response = EVE_FETCHER.get(token=jwt, endpoint=endpoint_with_query)

    user_info = user_response.json()
    headers = {"If-Match": user_info["_etag"], "X-HTTP-Method-Override": "PATCH"}
    endpoint = "accounts/%s" % user_id
    update = {"role": role}

    try:
        EVE_FETCHER.patch(endpoint=endpoint, token=jwt, headers=headers, json=update)

        logging.info({
                "message": "User(s) %s role changed to %s by %s" %
                           (user_info["email"], role, session["cidc_user_info"]["username"]),
                "category": "INFO-PORTAL-CHANGE-ROLE"})

        return True
    except RuntimeError:
        return False
