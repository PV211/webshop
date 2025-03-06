from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('add/<int:id>', add),
    path('remove/<int:id>', remove),
    path('count/', count)
]