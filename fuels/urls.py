from django.urls import path

from . import views


app_name = 'fuels'

urlpatterns = [
    path('', views.fuels, name='fuels'),
]
