from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_home, name='notes_home'),
    path('api/<int:note_id>/', views.get_note, name='get_note'),
    path('create/', views.create_note, name='create_note'),
    path('update/<int:note_id>/', views.update_note, name='update_note'), 
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('pin/<int:note_id>/', views.toggle_pin, name='toggle_pin'),
    path('reorder/', views.reorder_notes, name='reorder_notes'),
]