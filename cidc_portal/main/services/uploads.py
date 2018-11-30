import json
import logging
from cidc_utils.requests import SmartFetch

from constants import EVE_URL

EVE_FETCHER = SmartFetch(EVE_URL)


def get_olink_status(jwt: str) -> bool:
    """
    Query Olink uploads for this user. Join the uploads to a Data document to get the
    name of the uploaded file for displaying.

    Arguments:
        jwt {str} -- Requestor's JWT.

    Returns:
        list -- List of dictionaries describing uploads.
    """

    uploads_response = EVE_FETCHER.get(token=jwt, endpoint="olink")
    data_response = EVE_FETCHER.get(token=jwt, endpoint="data")

    status_list = []

    for upload in uploads_response.json()["_items"]:
        for data_entry in data_response.json()["_items"]:
            if data_entry["_id"] == upload["record_id"]:
                status_list.append({"id": upload["record_id"],
                                     "file_name": data_entry["file_name"],
                                     "validation_errors": upload["validation_errors"]})

    return status_list


def remove_data_record(jwt: str, data_id: str) -> bool:
    """
    In order to remove uploaded files we update the visibility flag on the data object to be false.

    :param jwt: User's JWT.
    :param data_id: Identifier of data record to be deleted.
    :return:
    """

    data_query = "data/%s" % data_id
    data_info = EVE_FETCHER.get(token=jwt, endpoint=data_query).json()
    data_etag = data_info["_etag"]

    payload = {"visibility": False}

    try:
        EVE_FETCHER.post(
            json=payload,
            headers={"If-Match": data_etag, "X-HTTP-Method-Override": "PATCH"},
            token=jwt,
            endpoint="data_vis/%s" % data_id,
        )

        logging.info({
                "message": "Data record %s removed" % data_id,
                "category": "INFO-PORTAL-REMOVE-DATA-RECORD"})

        return True
    except RuntimeError:
        return False
