from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegistrationForm
from django.contrib.auth.models import User
from demogithub.models import Profile, Repository
from datetime import datetime
import requests

# Create your views here.
def register(request):
    """Register a new user."""
    if request.method =='POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/login')
    else:
        form = RegistrationForm()
    
    context = {'form':form}
    return render(request,'registration/register.html',context)

def profile(request,user_name):
    profiles = Profile.objects.get(user_name=user_name)
    repos = Repository.objects.filter(owner=profiles)
    return render(request,'registration/profile.html',{'profiles':profiles,'repos':repos})

"""defining the api calls links"""
base_url = "https://api.github.com/users/"
additional_url = "/repos"

def button(request):
    user_name= request.user.username
    profile = Profile.objects.get(user_name=user_name)
    temp_user =profile.user
    temp_username=profile.user_name
    temp_name = profile.name
    temp_last_name = profile.last_name
    temp_repos=Repository.objects.filter(owner=profile)
    temp_repos.delete()
    profile.delete()
    profiles = Profile.objects.create(user=temp_user,name=temp_name,user_name=temp_username)
    profiles.last_name=temp_last_name
    
    """Updating the Profile Model using api call"""
    base_response = requests.get(base_url+str(user_name))
    if base_response.status_code==200:
        base_response_dict= base_response.json()
        bahutsare=base_response_dict["followers"]
        time_str=base_response_dict["updated_at"]
        time_which=datetime.strptime(time_str,'%Y-%m-%dT%H:%M:%SZ')
        profiles.followers = bahutsare
        profiles.last_updated = time_which
        profiles.save()
    
        """"Updating the repos corresponding to the profile"""
        repos_url=base_url+str(user_name)+additional_url
        new_base_response = requests.get(repos_url)
        new_base_response_dict = new_base_response.json()
        all_repos=dict()
        for fields in new_base_response_dict:
            all_repos[fields['name']]=fields['stargazers_count']
        all_repos=sorted(all_repos.items(), key =lambda kv:(kv[1], kv[0]),reverse=True)
        for repo in all_repos:
            new_repo,created = Repository.objects.get_or_create(name=repo[0],owner=profiles)
            new_repo.stars = repo[1]
            new_repo.save()
    
    repos = Repository.objects.filter(owner=profiles)
    return render(request,'registration/profile.html',{'profiles':profiles,'repos':repos})


def explore(request):
    """The page with all the people"""
    args={'user':request.user}
    all_users=Profile.objects.all()
    new_users={'users':all_users}
    return render(request,'explore.html',new_users)