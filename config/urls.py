from django.contrib import admin
from django.urls import path, include
from dashboard import views as dashboard_views  # ta page d'accueil

urlpatterns = [
    path('admin/', admin.site.urls),

    # page d'accueil Dashboard
    path('', dashboard_views.home, name='dashboard_home'),

    # page Planner
    path('planner/', include('planner.urls')),

    # si tu as d'autres apps
    path('notes/', include('notes.urls')),
]