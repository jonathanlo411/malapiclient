# Packages
import requests
import secrets

# Custom Errors
from errors import *

class malclient:
    
    ########### Meta ###########
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
        return f'{"Authorized " if self.authed else ""}MAL API Client, ID: {self.cid}'
    
    
    
    ########### Setters ###########
    def set_client_secret(self, secret: str):
        """
        Sets the secret to the client
        @params secret: Secret to add
        """
        self.cis = secret
        
    def set_token(self, token: dict):
        """
        Sets the token to the client
        @params token: dict in the format of JSON token response
        """
        self.token = token
        self.authed = True
        
        
        
    ########### Getters ###########
    def get_client_id(self):
        """
        Returns the Client ID
        """
        return self.cid
    
    def get_client_secret(self):
        """
        Returns the Client Secret if there is one, otherwise returns None
        """
        return self.cis
    
    def get_token(self):
        """
        Returns the token if there is one, otherwise returns None
        """
        return self.token
    
    
    
    ########### Authorizing and Tokens ###########
    def get_authorize_link(self):
        """ Returns the link to authorize
        """
        self.code = secrets.token_urlsafe(100)[:120]
        url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={self.cid}&code_challenge={self.code}'
        return url
    
    def generate_token(self, authorisation_code: str):
        """
        Generates MAL User token (via ZeroCrystal)
        @params authorisation_code: Code returned after redirected from the auth URL
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
        # Request
        response = requests.post(url, data)
        response.raise_for_status()
        token = response.json()
        response.close()
        self.token = token
        self.authed = True
        return token
    
    def refresh_token(self):
        """
        Refreshes the token currently assigned to the client
        """
        url = "https://myanimelist.net/v1/oauth2/token"
        data = {
            'client_id': self.cid,
            'client_secret': self.cis,
            'refresh_token': self.token['refresh_token'],
            'grant_type': 'refresh_token'
        }
        # Request
        response = requests.post(url, data)
        response.raise_for_status()
        token = response.json()
        response.close()
        self.token = token
        return token
    
    
    
    ########### MAL Endpoints ###########
    
    ### Anime ###
    def search_anime(self, query: str, **kwargs: iter):
        """
        Returns the results of an anime search
        @params query: What you want to search
        """
        url = f"https://api.myanimelist.net/v2/anime?q={query}"
        # User Specified Scopes
        if "fields" in kwargs.keys():
            url += "&fields="
            for i in kwargs['fields']:
                url += f"{i},"
        if "limit" in kwargs.keys():
            url += f"&limit={kwargs['limit']}"
        # Request
        response = requests.get(url, headers= {
            'X-MAL-CLIENT-ID': self.cid
        })
        response.raise_for_status()
        results = response.json()
        response.close()
        return results
    
    def get_anime_details(self, anime_id: str, **kwargs: iter):
        """
        Returns anime details given
        @params anime_id: ID of the anime
        @params fields: Called when  fields={some sort of iterable. When querying for specific fields
        """
        url = f'https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'
        # User Specified Scopes
        if "fields" in kwargs.keys():
            url = f'https://api.myanimelist.net/v2/anime/{anime_id}?fields='
            for i in kwargs['fields']:
                url += f"{i},"
        # Request
        response = requests.get(url, headers= {
            'X-MAL-CLIENT-ID': self.cid
        })
        response.raise_for_status()
        token = response.json()
        response.close()
        return anime_stats
    
    def get_anime_ranking(self, ranking_type="all", **kwargs: iter):
        """
        Returns the anime rankings
        @params ranking_type: Type of ranking
        """
        url = f"https://api.myanimelist.net/v2/anime/ranking?ranking_type={ranking_type}"
        # User Specified Scopes
        if "fields" in kwargs.keys():
            url += "&fields="
            for i in kwargs['fields']:
                url += f"{i},"
        if "limit" in kwargs.keys():
            url += f"&limit={kwargs['limit']}"
        if "offset" in kwargs.keys():
            url += f"&offset={kwargs['offset']}"
        # Request
        response = requests.get(url, headers= {
            'X-MAL-CLIENT-ID': self.cid
        })
        response.raise_for_status()
        results = response.json()
        response.close()
        return results
    
    def get_anime_seasonal(self, year, season, **kwargs: iter):
        """
        Returns the anime during the specified season and year
        @params year: Year of season you are searching for
        @params season: Specific season (Fall, Winter, etc.)
        """
        url = f"https://api.myanimelist.net/v2/anime/season/{year}/{season.lower()}"
        # User Specified Scopes
        if len(kwargs) != 0:
            url += "?"
            if "fields" in kwargs.keys():
                url += "&fields="
                for i in kwargs['fields']:
                    url += f"{i},"
            if "limit" in kwargs.keys():
                url += f"&limit={kwargs['limit']}"
            if "offset" in kwargs.keys():
                url += f"&offset={kwargs['offset']}"
            if "sort" in kwargs.keys():
                url += f"&sort={kwargs['sort']}"
        # Request
        response = requests.get(url, headers= {
            'X-MAL-CLIENT-ID': self.cid
        })
        response.raise_for_status()
        results = response.json()
        response.close()
        return results

    def get_anime_suggestions(self, **kwargs):
        url = "https://api.myanimelist.net/v2/anime/suggestions"
        # User Specified Scopes
        if len(kwargs) != 0:
            url += "?"
            if "fields" in kwargs.keys():
                url += "&fields="
                for i in kwargs['fields']:
                    url += f"{i},"
            if "limit" in kwargs.keys():
                url += f"&limit={kwargs['limit']}"
            if "offset" in kwargs.keys():
                url += f"&offset={kwargs['offset']}"
        # Request
        response = requests.get(url, headers = {
            "Authorization": f"Bearer {self.token['access_token']}"
        })
        response.raise_for_status()
        results = response.json()
        response.close()
        return results
