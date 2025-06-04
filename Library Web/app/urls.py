from django.urls import path
from . import views

urlpatterns = [
    path('query-examples/', views.query_examples, name='query_examples'),
]
