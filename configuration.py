from __future__ import (print_function, unicode_literals, division, absolute_import)
from builtins import open
from future import standard_library
standard_library.install_aliases()
from builtins import object
import pickle


class Configuration(object):
    # To get credentials visit https://developer.spotify.com/my-applications/
    credentials_file = "credentials.pickle"
    client_id = None
    client_secret = None
    auth_token = None

    @staticmethod
    def store_credentials():
        with open(Configuration.credentials_file, 'wb') as f:
            pickle.dump((Configuration.client_id, Configuration.client_secret), f)

    @staticmethod
    def load_credentials():
        with open(Configuration.credentials_file, 'rb') as f:
            Configuration.client_id, Configuration.client_secret = pickle.load(f)

