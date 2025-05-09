from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    
    
    #counting number of members per cooperative
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
        ('chairperson', 'Chairperson'),
        ('vice', 'Vice'),
        ('secretary', 'Secretary'),
        ('treasurer', 'Treasurer'),
        ('committee', 'Committee Member'),
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
    farmer_group = models.ForeignKey(FarmerGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='group_members', db_index=True)
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
    
    # New fields
    sunflower_acreage = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total land available for sunflower cultivation")
    sunflower_planted = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Actual acreage planted with sunflowers")
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_members')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    system_id = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="External system ID for the member")
    
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

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, help_text="put 0 if no contact is provided")
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True, related_name='supplier_products', help_text="Products supplied by this supplier")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SupplierProduct(models.Model):
    CATEGORIES  = (
        ('agro_inputs', 'Agro Inputs'),
        ('phones', 'Phones'),
        
        ('others','Others')
        
    )
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supplier_products_list')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, blank=True, null=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.supplier.name}"

class PlantingAllocation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='planting_allocations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='planting_allocations')
    allocated_acres = models.DecimalField(max_digits=10, decimal_places=2, help_text="Number of acres allocated for this product")
    planting_date = models.DateField(null=True, blank=True, help_text="Date when planting was done")
    expected_harvest_date = models.DateField(null=True, blank=True, help_text="Expected date of harvest")
    actual_harvest_date = models.DateField(null=True, blank=True, help_text="Actual date of harvest")
    status = models.CharField(
        max_length=20,
        choices=(
            ('planned', 'Planned'),
            ('planted', 'Planted'),
            ('growing', 'Growing'),
            ('harvested', 'Harvested'),
            ('cancelled', 'Cancelled')
        ),
        default='planned'
    )
    notes = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='planting_allocations')
    planting_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Number of seeds/seedlings planted or number of bee hives")
    planting_quantity_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='planting_allocations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Planting Allocation'
        verbose_name_plural = 'Planting Allocations'
        indexes = [
            models.Index(fields=['member', 'product']),
            models.Index(fields=['planting_date', 'expected_harvest_date']),
        ]

    def __str__(self):
        return f"{self.member} - {self.product} ({self.allocated_acres} acres)"

    def clean(self):
        # Validate that total allocated acres don't exceed member's total land
        if self.allocated_acres:
            total_allocated = PlantingAllocation.objects.filter(
                member=self.member
            ).exclude(
                pk=self.pk
            ).aggregate(
                total=models.Sum('allocated_acres')
            )['total'] or 0
            
            if total_allocated + self.allocated_acres > self.member.land_acres:
                raise ValidationError(
                    f"Total allocated acres ({total_allocated + self.allocated_acres}) exceeds member's total land ({self.member.land_acres} acres)"
                )

    def get_planting_quantity_display(self):
        if self.planting_quantity_unit:
            return f"{self.planting_quantity} {self.planting_quantity_unit.name}"
        return str(self.planting_quantity) if self.planting_quantity else "-"

class Collection(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='collections')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='collections')
    planting_allocation = models.ForeignKey(PlantingAllocation, on_delete=models.CASCADE, related_name='collections', null=True, blank=True)
    collection_date = models.DateField(help_text="Date when the product was collected")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity of product collected")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='collections')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per unit")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total price (quantity * unit_price)")
    quality_grade = models.CharField(
        max_length=20,
        choices=(
            ('A', 'Grade A'),
            ('B', 'Grade B'),
            ('C', 'Grade C'),
            ('D', 'Grade D')
        ),
        default='A'
    )
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_collections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
        indexes = [
            models.Index(fields=['member', 'product']),
            models.Index(fields=['collection_date']),
            models.Index(fields=['planting_allocation']),
        ]

    def __str__(self):
        return f"{self.member} - {self.product} ({self.quantity} {self.unit})"

    def save(self, *args, **kwargs):
        # Calculate total price before saving
        if self.quantity and self.unit_price:
            self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def clean(self):
        # Validate that collection date is not in the future
        if self.collection_date and self.collection_date > timezone.now().date():
            raise ValidationError("Collection date cannot be in the future")
        
        # Validate that quantity is positive
        if self.quantity and self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero")
        
        # Validate that unit price is positive
        if self.unit_price and self.unit_price <= 0:
            raise ValidationError("Unit price must be greater than zero")
        
        # Validate that planting allocation matches the product
        if self.planting_allocation and self.planting_allocation.product != self.product:
            raise ValidationError("Planting allocation product does not match collection product")

class LoanSupplier(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class CreditManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"

    class Meta:
        ordering = ['user__first_name']

class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('nottaken', 'Not Taken'),
        ('disbursed', 'Disbursed'),
        ('repaid', 'Repaid'),
        ('defaulted', 'Defaulted'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
    national_id = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    request_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    credit_manager = models.ForeignKey(CreditManager, on_delete=models.SET_NULL, null=True)
    loan_supplier = models.ForeignKey(LoanSupplier, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Loan {self.id} - {self.member}"

    class Meta:
        ordering = ['-request_date']


