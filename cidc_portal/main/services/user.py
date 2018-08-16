import datetime
import logging
import json

from flask import session

from email.utils import formatdate
from time import mktime

from constants import EVE_URL

from cidc_portal.main.forms.registration import RegistrationForm

from cidc_utils.requests import SmartFetch

EVE_FETCHER = SmartFetch(EVE_URL)


def update_user_info(jwt: str, form: RegistrationForm):
    """
    Takes the User Registration form and updates the user's account through an Eve endpoint.
    :param jwt: Users JWT in String
    :param form: WTForm Object for Registration form.
    :return:
    """
    user_response = EVE_FETCHER.get(token=jwt, endpoint='accounts_update')

    user_info = user_response.json()['_items'][0]

    headers = {
        'If-Match': user_info['_etag']
    }

    endpoint = 'accounts_update/%s' % user_info["_id"]

    timestamp = mktime(datetime.datetime.now(datetime.timezone.utc).timetuple())

    update = {
        "first_n": form.first_n.data,
        "last_n": form.last_n.data,
        "preferred_contact_email": form.contact_email.data,
        "organization": form.organization.data,
        "registered": True,
        "position_description": form.cidc_role.data,
        "registration_submit_date": formatdate(timeval=timestamp,
                                               localtime=False,
                                               usegmt=True)
    }

    EVE_FETCHER.patch(endpoint=endpoint,
                      token=jwt,
                      headers=headers,
                      json=update)


def get_user_info(jwt: str):
    """
    Grab the user's basic account info via an Eve endpoint.
    See ingestion API Accounts Schema for return format.
    :param jwt:
    :return:
    """
    try:
        user_response = EVE_FETCHER.get(token=jwt, endpoint='accounts_info')

        user_info = user_response.json()['_items'][0]

        return user_info
    except RuntimeError:
        logging.info({
            'message': "Runtime Error while fetching user info.",
            'category': 'INFO-PORTAL_TO_INGESTION-API'
        })
        return None


def get_trials(jwt: str, current_user: str):
    """
    Grab a listing of trial's user is a collaborator on from an Eve endpoint.
    :param jwt:
    :return:
    """

    trial_params = {'collaborators': current_user}
    endpoint_with_query = "trials?where=%s" % (json.dumps(trial_params))

    try:
        trials_response = EVE_FETCHER.get(token=jwt, endpoint=endpoint_with_query)
        return trials_response.json()['_items']
    except RuntimeError:
        return None


def get_cimac_biofox_user_home_data(jwt: str):
    """
    Pull together some information about the user from an Eve endpoint and
    put it in a dictionary.
    :param jwt:
    :return:
    """
    cimac_user_data = dict()

    cimac_user_data["gcp_upload_permission"] = None
    cimac_user_data["trials"] = get_trials(jwt, session["cidc_user_info"]["username"])

    return cimac_user_data





