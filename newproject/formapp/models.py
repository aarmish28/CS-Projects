from django.db import models

class Applicant(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    PROGRAM_CHOICES = [
        ('bachelor', 'Bachelor'),
        ('adp', 'ADP'),
    ]

    FULL_NAME_MAX_LENGTH = 25
    CNIC_MAX_LENGTH = 15

    full_name = models.CharField(max_length=FULL_NAME_MAX_LENGTH)
    email_id = models.EmailField()
    phone_no = models.CharField(max_length=13)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    cnic = models.CharField(max_length=CNIC_MAX_LENGTH)
    address = models.TextField()
  
    state_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    program_type = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    name_of_program = models.CharField(max_length=100)
    reason_to_join = models.CharField(max_length=100)

    school_name = models.CharField(max_length=200)
    starting_year = models.PositiveIntegerField()
    ending_year = models.PositiveIntegerField()
    obtained_marks = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    certification_choices = [
        ('Inter', 'Intermediate'),
        ('A-Levels', 'A-Levels'),
        ('DP Program', 'DP Program'),
    ]
    degree_level = models.CharField(choices=certification_choices, max_length=20)
    subject_group_choices = [
        ('Pre-Medical', 'Pre Medical'),
        ('Pre-Engineering', 'Pre Engineering'),
        ('Art & Humanities', 'Art & Humanities'),
        ('Intermediate with CS (ICS)', 'Intermediate with CS (ICS)'),
        ('I.Com', 'I.Com'),
        ('DAE Program', 'DAE Program'),
    ]
    subject_group = models.CharField(choices=subject_group_choices, max_length=50)
    institute_name = models.CharField(max_length=200)
    starting_year = models.PositiveIntegerField()
    ending_year = models.PositiveIntegerField()
    part_one_obtained_marks = models.PositiveIntegerField()
    part_two_obtained_marks = models.PositiveIntegerField(blank=True, null=True)
    merit_based = models.BooleanField(default=False)
    internship_based = models.BooleanField(default=False)
    earn_while_you_learn = models.BooleanField(default=False)
    kin_already_studying = models.BooleanField(default=False)
