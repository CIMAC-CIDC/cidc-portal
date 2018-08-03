from constants import URL_PREFIX
from cidc_portal.main.services.user import get_user_info


def url_for_with_prefix(url: str):
    """
    If we are serving the application under an existing URL path, we can
    use this to append a prefix to the URLs.

    Set PORTAL_URL_PREFIX in the environment, empty string for local development.
    :param url:
    :return:
    """
    return "%s%s" % (URL_PREFIX, url)


def base_user_info(session):
    session["cidc_user_info"] = get_user_info(session["jwt_token"])

    if session["cidc_user_info"] is None:
        return dict()
    else:
        return dict(user_role=session["cidc_user_info"]["role"],
                    user_name=session["cidc_user_info"]["username"],
                    clinical_trials_status_url=url_for_with_prefix("/trials-summary"),
                    cimac_biofx_home_url=url_for_with_prefix("/cimac_biofx/home"),
                    admin_home_url=url_for_with_prefix("/admin/home"),
                    privacy_url=url_for_with_prefix("/privacy")
                    )
