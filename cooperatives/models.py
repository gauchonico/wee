from django.db import models
from django.contrib.auth.models import User

class Unit(models.Model):
    name = models.CharField(max_length=100)  # e.g. "Kilogram", "Piece", "Litre"
    symbol = models.CharField(max_length=10)  # e.g. "kg", "pc", "L"
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_units')

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        ordering = ['name']
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

class Product(models.Model):
    name = models.CharField(max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_products')

    def __str__(self):
        return f"{self.name} ({self.unit.symbol})"

    class Meta:
        ordering = ['name']
        unique_together = ['name']

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='prices')
    effective_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_prices')

    def __str__(self):
        return f"{self.product.name} - {self.price} per {self.unit.symbol} ({self.effective_date})"

    class Meta:
        ordering = ['-effective_date']
        unique_together = ['product', 'effective_date']

class District(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class County(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='counties')
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.district.name})"

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Counties"

class SubCounty(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='subcounties')
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.county.name})"

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Sub Counties"

class Parish(models.Model):
    name = models.CharField(max_length=100)
    subcounty = models.ForeignKey(SubCounty, on_delete=models.CASCADE, related_name='parishes')
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.subcounty.name})"

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Parishes"

class Village(models.Model):
    name = models.CharField(max_length=100)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name='villages')
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.parish.name})"

    class Meta:
        ordering = ['name']

class PaymentMode(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Cooperative(models.Model):
    FPO_TYPES = (
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('tertiary', 'Tertiary'),
    )
    logo = models.ImageField(upload_to='cooperatives/logos/', null=True, blank=True)
    fpo_name = models.CharField(max_length=255)
    fpo_type = models.CharField(max_length=20, choices=FPO_TYPES)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True, blank=True)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    members = models.IntegerField(default=0)
    collections = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    registration_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.fpo_name
    
    class Meta:
        verbose_name = 'Cooperative'
        verbose_name_plural = 'Cooperatives'

class FarmerGroup(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True, blank=True)
    parish = models.ForeignKey(Parish, on_delete=models.SET_NULL, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, related_name='farmer_groups')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='farmer_groups')
    is_VSLA = models.BooleanField(default=False, verbose_name="Is VSLA")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = 'Farmer Group'
        verbose_name_plural = 'Farmer Groups'

class Member(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    ROLE_CHOICES = (
        ('chairman', 'Chairman'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer'),
        ('member', 'Member'),
    )
    
    name = models.CharField(max_length=255)
    member_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, related_name='cooperative_members')
    farmer_group = models.ForeignKey(FarmerGroup, on_delete=models.CASCADE, related_name='group_members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.member_id})"
    
    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'


