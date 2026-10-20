from django.urls import path

from . import views


app_name = 'refuelings'

urlpatterns = [
    path('', views.refuelings, name='refuelings'),
    path(
        '<int:refueling_id>/',
        views.refueling_detail,
        name='refueling_detail'
    ),
]
