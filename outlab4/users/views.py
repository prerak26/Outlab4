from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegistrationForm
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    """Register a new user."""
    if request.method =='POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/demogithub')
    else:
        form = RegistrationForm()
    
    context = {'form':form}
    return render(request,'registration/register.html',context)

def profile(request):
    args={'user':request.user}
    return render(request,'registration/profile.html',args)