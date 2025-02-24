from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('contact/', contact),
    path('login/', signin),
    path('register/', register),
    path('signout/', signout),
    path('consult/', xai_consultant),
]