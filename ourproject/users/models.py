from django.db import models
from django.contrib.auth.models import AbstractUser

import random
import string


class User(AbstractUser):
    is_user=models.BooleanField('is_user',default=False)
    is_staff=models.BooleanField('is_user',default=False)
    is_admin=models.BooleanField('is_user',default=False)

    location=models.CharField(max_length=255,null=True,blank=True)
    profile=models.ImageField(upload_to="profile/user_profile/")
    latitude=models.CharField(max_length=255,null=True,blank=True)
    longitude=models.CharField(max_length=255,null=True,blank=True)
    
    about=models.CharField(max_length=255,null=True,blank=True)
    def save(self, *args, **kwargs):
        if self.is_superuser and not self.is_admin:
            self.is_admin=True
            self.is_staff=True
            self.location=""
        super().save(*args, **kwargs)

class emailverification(models.Model):
    email=models.CharField(max_length=255, null=True, blank=True)
    token=models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.email
    

class Courier(models.Model):
    courier_id = models.CharField(max_length=10, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_couriers')
    accepted_at = models.DateTimeField(null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    destination_address = models.CharField(max_length=255, null=True, blank=True)
    destination_received_by =models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='destination_accepted_by')
    destination_received_at = models.DateTimeField(null=True, blank=True)
    checkpoint_1 = models.BooleanField(default=False)
    checkpoint_2 = models.BooleanField(default=False)
    checkpoint_3 = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    status=models.BooleanField(default=False)
    lattitude=models.CharField(max_length=255,null=True,blank=True)
    longitude=models.CharField(max_length=255,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.courier_id:
            self.courier_id = generate_courier_id()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.courier_id} - {str(self.sender)}'

def generate_courier_id():
    length = 8
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class CourierImage(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name='images')
    sent_by_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sent_courier_images')
    image = models.ImageField(upload_to='courier_images')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='uploaded_courier_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.courier.courier_id} - {self.sent_by_user.username} - {self.uploaded_at}'
    

class Complaint(models.Model):
    complaint_by = models.ForeignKey(User, on_delete=models.CASCADE)
    error_courier_id = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    issue=models.CharField(max_length=255,blank=True)
    def __str__(self):
        return f"Complaint #{self.pk} - Courier ID: {self.courier_id}"
    

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name