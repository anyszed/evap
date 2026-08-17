from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_views.home, name='dashboard_home'),
    path('planner/', include('planner.urls')),
    path('notes/', include('notes.urls')),
    path('calendar/', include('calendar_app.urls')),
    path('timer/', include('timer.urls')),
    path('grades/', include('grades.urls')),
]

# En prod le site tourne derrière gunicorn (pas `runserver`), qui est le
# seul à servir /static/ automatiquement en DEBUG=True. Sans whitenoise ni
# route dédiée, tout /static/... renvoie 404 sous gunicorn — cette route
# reproduit explicitement ce que `runserver` fait déjà en local.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()