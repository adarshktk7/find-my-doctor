from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    usertype=models.CharField(max_length=100)

class Doctor(models.Model):
    doc=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    specilization=models.CharField(max_length=100)
    hospital=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    location=models.CharField(max_length=100)

class Patient(models.Model):
    pat=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=100)
    place=models.CharField(max_length=100)

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) 
    patient_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    symptoms = models.TextField(blank=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
