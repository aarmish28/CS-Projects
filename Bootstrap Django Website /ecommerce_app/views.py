from django.shortcuts import render, redirect,get_object_or_404
from .models import Crud

def crud(request):

    emp = Crud.objects.all()

    context = {
        'emp': emp,

    }
    return render(request,'index.html',context)

def add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        emp=Crud(
            name = name,
            email= email,
            address=address,
            phone=phone,
        )
        emp.save()
        return redirect('index')

    return render(request,'index.html')

def edit(request):

     emp = Crud.objects.all()
     
     context = {
        'emp': emp,

    }
     return redirect(request, 'index.html',context)

def update(request,id):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        emp=Crud(
            id=id,
            name = name,
            email= email,
            address=address,
            phone=phone,
        )
        emp.save()
        return redirect('index')


    return redirect(request, 'index.html',)

def delete(request,id):
     
   emp = get_object_or_404(Crud, id=id)
   if request.method == 'POST':
        emp.delete()
        return redirect('employee_list')  # Redirect to the employee list page after successful deletion
   return render(request, 'index.html', {'emp': emp})