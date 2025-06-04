from django.shortcuts import render, HttpResponse,get_object_or_404
from .models import Employee,Role,Department,Book,Meeting,Expenses,Training,Task,Payroll,Feedback,Attendance
from datetime  import datetime
from django.db.models import  Q

# Create your views here.
def index(request):
    return render(request,"index.html")

def  view_all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    print(context)
    return render(request,'view_all_emp.html',context)
def  add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp =  Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id=dept, role_id=role, hire_data=datetime.now())
        new_emp.save()
        return HttpResponse("University Employee Added Sucessfully")
    elif request.method=='GET':
        return render(request,'add_emp.html')
    else:
        return HttpResponse("An Exceptional Error Occured, Employee has not been added")        

     # return render(request, 'add_emp.html')

def remove_emp(request, emp_id=0):
     if emp_id:
          try:
               emp_to_be_removed = Employee.objects.get(id=emp_id)
               emp_to_be_removed.delete()
               return HttpResponse("Employee Removed Successfully")
          except:
               return HttpResponse("Please Enter the Valid Employee ID")
     emps=Employee.objects.all()
     context = {
               'emps' : emps
          }
     return render(request, 'remove_emp.html', context)


def  filter_emp(request):
     if request.method == "POST":
      name = request.POST['name']
      dept = request.POST['dept']
      role = request.POST['role']
      emps = Employee.objects.all()
      if name:
         emps = emps.filter(Q(first_name__icontainns = name)) | Q(last_name__icotains = name )
      if  dept:
         emps = emps/filter(dept__name__icontains =  dept)
      if role:
         emps = emps.filter(role__name__icontains = role )

      context = {
         'emps' : emps
     }
      return render(request,'view_all_emp.html',context)
     elif request.method=='GET':
      return render(request,'filter_emp.html')
     else:
      return HttpResponse("An Exception Occured")
     
from .models import Book

def  aarmish(request):
    books =  Book.objects.all()
    context = {
        'books'  : books
    }
    return render(request, 'goku.html', context)

def employeemeeting(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        dept_id = request.POST['dept']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        dept = Department.objects.get(id=dept_id)

        meeting = Meeting(name=name, description=description, dept=dept, start_time=start_time, end_time=end_time)
        meeting.save()

        return HttpResponse("Meeting Added Successfully")
    elif request.method == "GET":
        return render(request, 'employeemeeting.html')
    else:
        return HttpResponse("An Error Occurred")
    
def employeeexpenses (request):
    
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        amount = int(request.POST['amount'])
        date = request.POST['date']
        
    
        expenses = Expenses(name=name, description=description,amount=amount,date=date)
        expenses.save()

        return HttpResponse("Expenses Added Successfully")

    elif request.method == "GET":
        return render(request, 'employeeexpenses.html')
    else:
        return HttpResponse("An Error Occurred")
    
def employeetraining (request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        dept_id = request.POST['dept']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

    
        dept = Department.objects.get(id=dept_id)

        training = Training(name=name, description=description, dept=dept, start_time=start_time, end_time=end_time)
        training.save()

        return HttpResponse("Training Added Successfully")

    elif request.method == "GET":
        return render(request, 'employeetraining.html')
    else:
        return HttpResponse("An Error Occurred")

def employeetask (request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        dept_id = request.POST['dept']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

    
        dept = Department.objects.get(id=dept_id)

        employee_task= Task(name=name, description=description, dept=dept, start_time=start_time, end_time=end_time)
        employee_task.save()

        return HttpResponse("Task Added Successfully")

    elif request.method == "GET":
        return render(request, 'employeetask.html')
    else:
        return HttpResponse("An Error Occurred")


def employeepayroll (request):
    if request.method == "POST":
        name = request.POST['name']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        basic_pay = int(request.POST['basic_pay'])
        overtime_pay = int(request.POST['overtime_pay'])
        tax_deducted = int(request.POST['tax_deducted'])
        net_pay = int(request.POST['net_pay'])

        payroll = Payroll(name=name, start_time=start_time, end_time=end_time, basic_pay=basic_pay, overtime_pay=overtime_pay, tax_deducted=tax_deducted, net_pay=net_pay)
        payroll.save()
        return HttpResponse("Payroll Added Successfully")

    elif request.method == "GET":
        return render(request, 'employeepayroll.html')
    else:
        return HttpResponse("An Error Occurred")
    

def location (request):
    return render (request,"location.html")

def employeefeedback (request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        content = request.POST['content']
        
        feedback = Feedback(name=name, email=email, content=content)
        feedback.save()
        return HttpResponse("Feedback Added Successfully")

    elif request.method == "GET":
        return render(request, 'employeefeedback.html')
    else:
        return HttpResponse("An Error Occurred")


def employeeimages (request):
    return render(request,"employeeimages.html")


def attendance(request):
    if request.method == 'POST':
        date = request.POST['date']
        status = request.POST['status']
        employee_id = request.POST['employee']

        employee = get_object_or_404(Employee, id=employee_id)
        attendance = Attendance(employee=employee, date=date, status=status)
        attendance.save()

        return HttpResponse("Attendance added successfully")
    else:
        employees = Employee.objects.all()
        return render(request, 'attendance.html', {'employees': employees})
def viewattendance(request):
    attendances = Attendance.objects.all()
    context = {
        'attendances': attendances
    }
    return render(request, 'viewattendance.html', context)



