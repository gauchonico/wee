from django.db import models
from django.contrib.auth.models import User
from cooperatives.models import District, FarmerGroup
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    date_joined = models.DateField(null=True, blank=True)
    districts = models.ManyToManyField(District, blank=True)
    farmer_groups = models.ManyToManyField(FarmerGroup, blank=True)
    is_active = models.BooleanField(default=True)
    is_credit_manager = models.BooleanField(default=False, help_text="Indicates if this agent can also act as a credit manager")
    farmers_profiled = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    def get_active_incentive(self):
        """Get the currently active incentive for this agent"""
        return self.incentives.filter(is_active=True).first()

    def get_total_incentive_amount(self):
        """Get the total incentive amount for the agent based on global incentive rate"""
        active_incentive = Incentive.objects.filter(is_active=True).first()
        if active_incentive:
            return active_incentive.calculate_total_incentive(self.farmers_profiled)
        return 0

    def create_user_account(self):
        """Create a user account for this agent if it doesn't exist"""
        if not self.user:
            username = f"{self.first_name.lower()}_{self.last_name.lower()}"
            email = self.email or f"{username}@example.com"
            
            # Check if username already exists
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password='default_password',  # Agent should change this on first login
                first_name=self.first_name,
                last_name=self.last_name,
                is_staff=True  # Give them staff access
            )
            self.user = user
            self.save()
            return user
        return self.user

class Incentive(models.Model):
    price_per_farmer = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Global Incentive - {self.price_per_farmer} per farmer"

    def calculate_total_incentive(self, farmers_count):
        """Calculate total incentive amount based on number of farmers"""
        if not self.is_active:
            return 0
        return self.price_per_farmer * farmers_count

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Global Incentive'
        verbose_name_plural = 'Global Incentives'

    def save(self, *args, **kwargs):
        # If this incentive is being set as active, deactivate all others
        if self.is_active:
            Incentive.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
