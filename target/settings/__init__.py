import os
import importlib

from .base import *

ENV_ROLE = os.getenv('ENV_ROLE', 'local')
environment_settings = importlib.import_module(f'target.settings.{ENV_ROLE}_settings')

globals().update(vars(environment_settings))

if ENV_ROLE == 'heroku':
    globals()['MIDDLEWARE'].append('whitenoise.middleware.WhiteNoiseMiddleware')
