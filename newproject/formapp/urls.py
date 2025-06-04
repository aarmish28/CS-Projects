from django.urls import path
from formapp import views


urlpatterns = [

    path('application/', views.scholarship_application, name='application'),
    path('success_page/', views.success_page, name='success_page'),

    
]

    



