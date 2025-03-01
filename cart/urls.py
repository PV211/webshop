from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('checkout/', checkout),
    path('add/<int:id>', add),
    path('remove/<int:id>', remove),
    path('change/<int:id>', change),
    path('count/', count)
]