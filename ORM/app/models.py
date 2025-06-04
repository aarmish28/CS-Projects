from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Form(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return f"{self.form.title} - {self.user.username} - {self.submission_date}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class FormTag(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.form.title} - {self.tag.name}"
