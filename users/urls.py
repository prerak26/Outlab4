from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns =[
    #Using the Django default authorization urls
    path('',include('django.contrib.auth.urls')),
    #Registration Page
    path('register/',views.register,name='register'),
    # path('profile/',views.profile,name='profile'),
    path('profile/<str:user_name>/', views.profile, name='profile'),
    path('profile/',views.button,name='refresh'),
    path('explore/',views.explore,name='explore'),
]