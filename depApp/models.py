from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    idproof = models.FileField(upload_to="Proof")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Counselor(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    qual = models.CharField(max_length=50)
    proof = models.FileField(upload_to="Proof")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Tests(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    status = models.CharField(max_length=20,default='Active')

class Prediction(models.Model):
    date = models.DateField(auto_now_add=True)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=500,null=True)
    video = models.FileField(upload_to="prediction")
    status = models.CharField(max_length=20)

class Consultation(models.Model):
    date = models.DateField(auto_now_add=True)
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=20)

class Reports(models.Model):
    date = models.DateField(auto_now_add=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    report = models.CharField(max_length=200)
    document = models.FileField(null=True, blank=True)

class Message(models.Model):
    date = models.DateField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    sendby = models.CharField(max_length=20)

class Feedback(models.Model):
    date = models.DateField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=200)

