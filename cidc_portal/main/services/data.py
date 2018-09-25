import json
from cidc_utils.requests import SmartFetch

from constants import EVE_URL

EVE_FETCHER = SmartFetch(EVE_URL)


def delete_data(jwt: str, data_ids: List[str]) -> bool:
    """
    Attempts to delete a set of records.

    Arguments:
        jwt {str} -- Requestor's JWT.
        data_ids {List[str]} -- List of IDs for data to be deleted.

    Returns:
        bool -- True if succesful, else false.
    """
    query = {"$in": data_ids}
    endpoint_with_query = "data/?where=%s" % (json.dumps(query))
    try:
        EVE_FETCHER.delete(token=jwt, endpoint=endpoint_with_query)
        return True
    except RuntimeError:
        print("Deletion failed")
        return False
