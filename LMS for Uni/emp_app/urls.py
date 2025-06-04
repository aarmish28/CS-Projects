from django.urls import path, include
from  emp_app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
   path('',views.index,name="index"),
   path('view_all_emp',views.view_all_emp,name="view_all_emp"),
   path('add_emp',views.add_emp,name='add_emp'),
   path('remove_emp',views.remove_emp,name='remove_emp'),
   path("remove_emp/<int:emp_id>",views.remove_emp,name='remove_emp'),
   path('filter_emp',views.filter_emp,name='filter_emp'),
   path('aarmish', views.aarmish,name="aarmish"),
   path('employeemeeting',views.employeemeeting,name='employeemeeting'),
   path('employeeexpenses',views.employeeexpenses,name='employeeexpenses'),
   path('employeetraining',views.employeetraining,name='employeetraining'),
   path('employeetask',views.employeetask,name='employeetask'),
   path('employeepayroll',views.employeepayroll,name='employeepayroll'),
   path('location',views.location,name='location'),
   path('employeefeedback',views.employeefeedback,name='employeefeedback'),
   path('employeeimages',views.employeeimages,name='employeeimages'),
   path('attendance',views.attendance,name='attendance'),  
   path('viewattendance',views.viewattendance,name='viewattendance')
   

]
urlpatterns += staticfiles_urlpatterns()