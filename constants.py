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

FLASK_SECRET_KEY = env.get('FLASK_SECRET_KEY')

AUTH0_CALLBACK_URL = env.get('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
AUTH0_AUDIENCE = env.get('AUTH0_AUDIENCE')
ALGORITHMS = ["RS256"]

LOGGER = logging.getLogger('cidc-portal')
LOGGER.setLevel(logging.DEBUG)

if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = 'https://' + AUTH0_DOMAIN + '/userinfo'

if FLASK_SECRET_KEY is None:
    raise RuntimeError('FLASK_SECRET_KEY Configuration missing!')
