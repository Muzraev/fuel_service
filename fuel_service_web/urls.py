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


from django.conf import settings  # noqa: E402

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
