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
    collections = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    registration_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def member_count(self):
        """Returns the actual count of members in this cooperative"""
        return self.cooperative_members.count()
    
    def __str__(self):
        return f"{self.fpo_name} ({self.member_count} members)"
    
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
        ('vice', 'Vice'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer'),
        ('committee', 'Committee'),
        ('member', 'Member'),
    )
    
    ID_TYPE_CHOICES = (
        ('national_id', 'National ID'),
        ('passport', 'Passport'),
        ('drivers_license', 'Driver\'s License'),
        ('voters_card', 'Voter\'s Card'),
        ('refugee_id', 'Refugee ID'),
        ('other', 'Other'),
    )
    
    first_name = models.CharField(max_length=255, db_index=True)
    surname = models.CharField(max_length=255, db_index=True)
    other_name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, help_text="Member's date of birth")
    email = models.EmailField(max_length=255, null=True, blank=True)
    member_id = models.CharField(max_length=50, unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, db_index=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, related_name='cooperative_members', db_index=True)
    farmer_group = models.ForeignKey(FarmerGroup, on_delete=models.CASCADE, related_name='group_members', db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member', db_index=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    
    # GPS coordinates
    gps_coordinates = models.CharField(max_length=50, null=True, blank=True, help_text="GPS coordinates as a single string (e.g. '2.90091247,33.35992853')")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Latitude coordinate of the member's location")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Longitude coordinate of the member's location")
    
    # New fields
    is_verified = models.BooleanField(default=False, help_text="Whether the member has been verified")
    has_mobile_money = models.BooleanField(default=False, help_text="Whether the member has mobile money")
    is_refugee = models.BooleanField(default=False, help_text="Whether the member is a refugee")
    id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES, null=True, blank=True, help_text="Type of identification document")
    id_number = models.CharField(max_length=50, null=True, blank=True, help_text="Identification document number", db_index=True)
    
    # Land and production details
    land_acres = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Total land size in acres")
    shea_trees = models.IntegerField(null=True, blank=True, help_text="Number of shea trees")
    beehives = models.IntegerField(null=True, blank=True, help_text="Number of beehives")
    
    # Products cultivated (Many-to-Many relationship)
    products = models.ManyToManyField(Product, blank=True, related_name='member_products', help_text="Products cultivated by the member")
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_members')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        indexes = [
            models.Index(fields=['first_name', 'surname']),
            models.Index(fields=['created_at', 'cooperative']),
            models.Index(fields=['district', 'county', 'sub_county']),
        ]
        
    def __str__(self):
        return f"{self.surname}, {self.first_name} ({self.member_id})"
    
    def save(self, *args, **kwargs):
        # If gps_coordinates is provided but lat/long are empty, parse and set them
        if self.gps_coordinates and not (self.latitude and self.longitude):
            try:
                lat, lon = map(float, self.gps_coordinates.split(','))
                self.latitude = lat
                self.longitude = lon
            except (ValueError, TypeError):
                pass
        # If lat/long are provided but gps_coordinates is empty, format and set it
        elif self.latitude and self.longitude and not self.gps_coordinates:
            self.gps_coordinates = f"{self.latitude},{self.longitude}"
        super().save(*args, **kwargs)


