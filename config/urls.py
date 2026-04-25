from django.contrib import admin
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