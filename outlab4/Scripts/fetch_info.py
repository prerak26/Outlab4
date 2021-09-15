import requests
from demogithub.models import Profile

base_url="https://api.github.com/users/"

base_response = requests.get(base_url)
