import webbrowser
import secrets
import requests

class malclient:
    
    def __init__(self, client_id=None, client_secret=None):
        self.cid = client_id
        self.cis = client_secret
        self.authed = False
        if (client_id != None) and (client_secret != None):
            self.setup()
            self.authed = True
        
    def __repr__(self):
        return f'{"Authorized " if self.authed else ""}MAL API Client:\nClient ID: {self.cid}\nClient Secret: {self.cis}'
    
    def setup(self):
        code = secrets.token_urlsafe(100)[:120]
        url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={self.cid}&code_challenge={code}'
        webbrowser.open(url)
        response = input("Authorisation Code: ")

    def get_anime(self, anime_id):
        url = f'https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,main_picture,alternative_titles,synopsis,mean,rank,popularity,num_list_users,media_type,status,genres,my_list_status,num_episodes,start_season,source,studios'
        response = requests.get(url, headers= {
            'Authorization': 'X-MAL-CLIENT-ID'
        })
        response.raise_for_status()
        anime_stats = response.json()
        response.close()
        return anime_stats

