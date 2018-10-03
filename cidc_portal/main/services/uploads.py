import json
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


