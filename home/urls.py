from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('contact/', contact),
    path('about/', about),
    path('services/', services),
    path('login/', signin),
    path('register/', register),
    path('signout/', signout),
    path('consult/', xai_consultant),
]