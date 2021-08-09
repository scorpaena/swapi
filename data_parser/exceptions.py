class DoesNotExistError(Exception):
    """Raised when HTTP.status != 200"""

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"{self.url} has no data"
