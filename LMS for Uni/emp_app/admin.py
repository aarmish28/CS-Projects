from django.contrib import admin
from .models import Employee,Role,Department, Meeting, Expenses, Training, Attendance, Task, Payroll, Feedback,Book

# Register your models here.
admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Meeting)
admin.site.register(Expenses)
admin.site.register(Training)
admin.site.register(Attendance)
admin.site.register(Task)
admin.site.register(Payroll)
admin.site.register(Feedback)
admin.site.register(Book)
