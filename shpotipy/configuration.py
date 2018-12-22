from builtins import open, object
import pickle


class Configuration(object):
    # To get credentials visit https://developer.spotify.com/my-applications/
    credentials_file = "credentials.pickle"
    token_file = "token.pickle"
    client_id = None
    client_secret = None
    auth_token = None

    @staticmethod
    def store_credentials():
        with open(Configuration.credentials_file, "wb") as f:
            pickle.dump((Configuration.client_id, Configuration.client_secret), f)

    @staticmethod
    def load_credentials():
        with open(Configuration.credentials_file, "rb") as f:
            Configuration.client_id, Configuration.client_secret = pickle.load(f)

    @staticmethod
    def store_token():
        with open(Configuration.token_file, "wb") as f:
            pickle.dump(Configuration.auth_token, f)

    @staticmethod
    def load_token():
        with open(Configuration.token_file, "rb") as f:
            Configuration.auth_token = pickle.load(f)
