from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='grades_home'),

    # GET DATA (IMPORTANT)
    path('get_tables/', views.get_tables),

    # CREATE
    path('create_table/', views.create_table),
    path('add_subject/<int:table_id>/', views.add_subject),
    path('add_grade/<int:subject_id>/', views.add_grade),

    # DELETE
    path('delete_table/<int:table_id>/', views.delete_table),
    path('delete_subject/<int:subject_id>/', views.delete_subject),
    path('delete_grade/<int:grade_id>/', views.delete_grade),

    # UPDATE
    path('update_table/<int:table_id>/', views.update_table),
    path('update_subject/<int:subject_id>/', views.update_subject),
    path('update_grade/<int:grade_id>/', views.update_grade),
]