import re

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.views import serve as serve_static
from django.urls import path, include, re_path
from django.views.decorators.cache import cache_control
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
#
# Les fichiers ne portent pas de hash de contenu dans leur nom (pas de
# ManifestStaticFilesStorage/collectstatic en place), donc sans en-tête
# Cache-Control explicite le navigateur applique une politique heuristique
# et peut resservir un vieux CSS/JS en cache après un déploiement, sans
# même recontacter le serveur (constaté : le grand post-it du bloc-notes
# s'affichait avec l'ancien style tant qu'on ne rechargeait pas en forçant
# le cache). `no_cache=True` force une revalidation à chaque requête —
# Last-Modified/ETag permettent quand même un 304 rapide si le fichier n'a
# pas changé, donc pas de vrai coût, juste plus de garantie de fraîcheur.
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
            cache_control(no_cache=True, must_revalidate=True)(serve_static),
        ),
    ]