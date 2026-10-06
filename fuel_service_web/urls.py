from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('cars/', include('cars.urls')),
    path('fuels/', include('fuels.urls')),
    path(
        'refuelings/',
        include('refuelings.urls')
    ),
]


handler404 = 'homepage.views.page_not_found'
