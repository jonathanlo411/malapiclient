# Packages
import requests
import secrets

# Custom Errors
from errors import *

class malclient:
    
    def __init__(self, client_id, **kwargs):
        # Base
        self.authed = False
        self.cid = client_id
        self.cis = None
        self.code = None
        self.token = None
        
        # If Contains Client Secret
        if 'client_secret' in kwargs.keys():
            self.cis = kwargs['client_secret']
        
    def __repr__(self):
        return f'{"Authorized " if self.authed else ""}MAL API Client'
    
    def add_secret(self, secret):
        self.cis = secret
    
    def get_authorize_link(self):
        """ Returns the link to authorize
        """
        self.code = secrets.token_urlsafe(100)[:120]
        url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={self.cid}&code_challenge={self.code}'
        return url
    
    def generate_token(self, authorisation_code):
        """ Generates MAL User token (via ZeroCrystal)
        """
        if self.cis == None:
            raise NoClientSecretError
        url = 'https://myanimelist.net/v1/oauth2/token'
        data = {
            'client_id': self.cid,
            'client_secret': self.cis,
            'code': authorisation_code,
            'code_verifier': self.code,
            'grant_type': 'authorization_code'
        }
        response = requests.post(url, data)
        response.raise_for_status()
        token = response.json()
        response.close()
        self.token = token
        self.authed = True
        return token