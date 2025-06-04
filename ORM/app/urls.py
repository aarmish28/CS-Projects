from django.urls import path
from . import views

urlpatterns = [
    path('forms/', views.form_list, name='form_list'),
    path('forms/create/', views.create_form, name='create_form'),
    path('forms/edit/<int:form_id>/', views.edit_form, name='edit_form'),
    path('forms/delete/<int:form_id>/', views.delete_form, name='delete_form'),
]
