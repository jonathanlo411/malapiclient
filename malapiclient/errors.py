
class Error(Exception):
    """Base class for other exceptions"""
    pass

class NoClientSecretError(Error):
    def __str__(self):
        return "No Client Secret. You can add your Client Secret to your malclient by using malclient.add_secret()"
    pass

class NeedAuthentificationError(Error):
    def __str__(self):
        return "No Client Secret. You can add your Client Secret to your malclient by using malclient.add_secret()"
    pass