from django.db.models.signals import pre_delete
import requests
from datetime import datetime
base_url="https://api.github.com/users/"

additional_url = "/repos"

def search_for_profiles(user_name):
    base_response = requests.get(base_url+str(user_name))
    if base_response.status_code==200:
        base_response_dict= base_response.json()
        numberoffollowers=base_response_dict["followers"]
        time_str=base_response_dict["updated_at"]
        timehello=datetime.strptime(time_str,'%Y-%m-%dT%H:%M:%SZ')
    return (numberoffollowers,timehello)

def search_for_repos(user_name):
    repos_url=base_url+str(user_name)+additional_url
    base_response = requests.get(repos_url)
    base_response_dict = base_response.json()
    all_repos=dict()
    for fields in base_response_dict:
        all_repos[fields['name']]=fields['stargazers_count']
    all_repos=sorted(all_repos.items(), key =lambda kv:(kv[1], kv[0]),reverse=True)
    return all_repos