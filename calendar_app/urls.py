from django.urls import path
from . import views

urlpatterns = [
    path("", views.calendar_page, name="calendar"),
    path("events/", views.get_events),
    path("create/", views.create_event),
    path("update/<int:event_id>/", views.update_event),
]