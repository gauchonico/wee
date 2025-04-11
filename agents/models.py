from django.db import models
from django.contrib.auth.models import User
from cooperatives.models import District, FarmerGroup
from django.core.exceptions import ValidationError

class Agent(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    agent_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    date_joined = models.DateField(null=True, blank=True)
    districts = models.ManyToManyField(District, blank=True)
    farmer_groups = models.ManyToManyField(FarmerGroup, blank=True)
    is_active = models.BooleanField(default=True)
    farmers_profiled = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.agent_id})"

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if not self.phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return super().clean()
