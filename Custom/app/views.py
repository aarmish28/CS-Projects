from django.shortcuts import render, get_object_or_404, redirect
from .models import User

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User(username=username, email=email, password=password)
        user.save()
        return redirect('user_list')

    return render(request, 'user_form.html')

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.save()
        return redirect('user_list')

    return render(request, 'user_form.html', {'user': user})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    
    return render(request, 'user_confirm_delete.html', {'user': user})
