from django.shortcuts import render, redirect,get_object_or_404
from app.models import Crud

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

def update(request, id):
   
    emp =  Crud.objects.get(id=id)

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

       
        emp.name = name
        emp.email = email
        emp.address = address
        emp.phone = phone

        
        emp.save()

        return redirect('index')
  
    context = {'emp': emp}
    return render(request, 'update.html', context)


def delete(request, id):
    
    crud = Crud.objects.get(id=id)

  
    crud.delete()

    emp = Crud.objects.all()

    context = {'emp': emp}
    return render(request, 'index.html', context)
