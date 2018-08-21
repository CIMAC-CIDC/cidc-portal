#!/usr/bin/env python3
"""
Constants file for computing some environmental variables.
"""
import logging
from os import environ as env
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

URL_PREFIX = env.get("PORTAL_URL_PREFIX")

EVE_URL = env.get("EVE_URL")

VERIFY_URLS = env.get("VERIFY_URLS")

FLASK_SECRET_KEY = env.get('PORTAL_FLASK_SECRET_KEY')

AUTH0_CALLBACK_URL = env.get('PORTAL_AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = env.get('PORTAL_AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = env.get('PORTAL_AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = env.get('PORTAL_AUTH0_DOMAIN')
AUTH0_AUDIENCE = env.get('PORTAL_AUTH0_AUDIENCE')

SENDGRID_API_KEY = env.get('SENDGRID_API_KEY')
SEND_FROM_EMAIL = env.get('SEND_FROM_EMAIL', "no-reply@cimac-network.org")
CIDC_MAILING_LIST = env.get('CIDC_MAILING_LIST', "cidc@jimmy.harvard.edu")

SESSION_TIMEOUT_MINUTES = env.get('SESSION_TIMEOUT', 10)

ALGORITHMS = ["RS256"]

ADMIN_ROLE = "admin"
CIMAC_BIOFX_ROLE = "uploader"
REGISTRANT_ROLE = "registrant"

LOGGER = logging.getLogger('cidc-portal')
LOGGER.setLevel(logging.DEBUG)

if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = 'https://' + AUTH0_DOMAIN + '/userinfo'

if FLASK_SECRET_KEY is None:
    raise RuntimeError('FLASK_SECRET_KEY Configuration missing!')
