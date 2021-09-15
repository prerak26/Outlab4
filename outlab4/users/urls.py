from django.urls import path, include

app_name = 'users'
urlpatterns =[
    #Using the Django default authorization urls
    path('',include('django.contrib.auth.urls')),
]