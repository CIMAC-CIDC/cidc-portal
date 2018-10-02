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
    if "jwt_token" in session:
        session["cidc_user_info"] = get_user_info(session["jwt_token"])

        if session["cidc_user_info"] is not None:
            return dict(
                user_role=session["cidc_user_info"]["role"],
                user_name=session["cidc_user_info"]["username"],
                clinical_trials_status_url=url_for_with_prefix("/trials-summary"),
                cimac_biofx_home_url=url_for_with_prefix("/cimac_biofx/home"),
                cli_install_url=url_for_with_prefix("/cimac_biofx/cli-install"),
                olink_upload_url=url_for_with_prefix("/cimac_biofx/olink-upload"),
                admin_home_url=url_for_with_prefix("/admin/home"),
                privacy_url=url_for_with_prefix("/privacy"),
                logout_url=url_for_with_prefix("/logout"),
                user_info_url=url_for_with_prefix("/admin/user_info"),
            )
    return dict()
