from django.urls import path

from . import views


app_name = 'cars'

urlpatterns = [
    path('without-plans/', views.without_plans, name='without_plans'),
    path('by-slug/<slug:slug>/', views.car_by_slug, name='car_by_slug'),
    path('', views.cars, name='cars'),
    path(
        '<int:car_id>/',
        views.car_detail,
        name='car_detail'
    ),
]
