from django import forms
from .models import Applicant,VoucherForm

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['full_name', 'email_id', 'date_of_birth', 'address', 'phone_no','gender','cnic','state_name','country_name','program_type','name_of_program','reason_to_join',
                  'school_name', 'starting_year', 'ending_year', 'obtained_marks', 'total_marks','degree_level', 'subject_group', 'institute_name', 'starting_year', 'ending_year', 'part_one_obtained_marks', 'part_two_obtained_marks',
                  'merit_based', 'internship_based', 'earn_while_you_learn', 'kin_already_studying']
        
class Voucher(forms.ModelForm):
    class Meta:
        model = VoucherForm
        fields = '__all__'

