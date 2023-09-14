from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('spare/<int:spare_id>', spareOrderPage, name="spare")
]