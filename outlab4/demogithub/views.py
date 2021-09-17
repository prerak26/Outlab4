from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello World. You are welcome to the start of a legacy.")

def home(request):
    return render(request,'home.html')