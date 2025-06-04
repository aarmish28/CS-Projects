from django.shortcuts import render, redirect, get_object_or_404
from .models import Form
from django import forms

class FormCreateForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title', 'description']

def form_list(request):
    forms = Form.objects.all()
    return render(request, 'form_list.html', {'forms': forms})

def create_form(request):
    if request.method == 'POST':
        form = FormCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('form_list')
    else:
        form = FormCreateForm()
    return render(request, 'form_create.html', {'form': form})

def edit_form(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    if request.method == 'POST':
        form_edit = FormCreateForm(request.POST, instance=form)
        if form_edit.is_valid():
            form_edit.save()
            return redirect('form_list')
    else:
        form_edit = FormCreateForm(instance=form)
    return render(request, 'form_edit.html', {'form_edit': form_edit, 'form': form})

def delete_form(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    if request.method == 'POST':
        form.delete()
        return redirect('form_list')
    return render(request, 'form_delete.html', {'form': form})
