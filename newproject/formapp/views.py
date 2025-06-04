from django.shortcuts import render, redirect
from .forms import ApplicantForm

def scholarship_application(request):
    if request.method == 'POST':
        print('POST request received:', request.POST)
        applicant_form = ApplicantForm(request.POST)
        
       
        print('form.errors')
        if applicant_form.is_valid():
            # Save Applicant Information
           applicant_form.save()

    
            # Redirect to a success page or display a success message
        return redirect('success_page')

    else:
        applicant_form = ApplicantForm()
       

    context = {
        'applicant_form': applicant_form,
     
    }
    return render(request, 'form.html', context)

def success_page(request):
    return render(request, 'success_page.html')
print('View executed')