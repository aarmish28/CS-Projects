from django.db import models

# Create your models here.
class  Department(models.Model):
    name = models.CharField(max_length=100, null=False)
    location= models.CharField(max_length=100)

    def  __str__(self):
        return self.name
    
class  Role(models.Model):
    name = models.CharField(max_length=100, null=False)
    def  __str__(self):
        return self.name
class Employee(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name= models.CharField(max_length=100)
    dept = models.ForeignKey(Department,on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus =  models.IntegerField(default=0)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)
    hire_data =models.DateField()

    def  __str__(self):
        return "%s %s %s" %(self.first_name,self.last_name,self.phone)
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover = models.ImageField(upload_to = 'images/')

    def __str__(self):
        return self.title
   
    
class Meeting(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

class Expenses(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=100)
    amount = models.IntegerField()
    date = models.DateTimeField()
    
    def __str__(self):
        return self.name

class Training(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def __str__(self):
        return self.name  
    
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def __str__(self):
        return self.name

class Payroll(models.Model):
      name = models.CharField(max_length=200)
      start_time=models.DateTimeField()
      end_time= models.DateTimeField()
      basic_pay = models.IntegerField()
      overtime_pay = models.IntegerField()
      tax_deducted =models.IntegerField()
      net_pay = models.IntegerField()
      
      def __str(self):
          return self.name

class Feedback(models.Model):
     name = models.CharField(max_length=100)
     email = models.TextField()
     content = models.TextField()
    
    
     def __str(self):
          return self.name    
     
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])

    def __str__(self):
        return f"{self.employee} on {self.date}: {self.status}"