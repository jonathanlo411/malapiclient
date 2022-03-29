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