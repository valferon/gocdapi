import requests
from ..config import *

class GocdEndpoint():
    def __init__(self):
        self.server_url = server_url