from django.contrib import admin
from .models import (
    District, County, Price, SubCounty, Parish, Village, PaymentMode,
    Cooperative, FarmerGroup, Member, Product, Unit
)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at', 'updated_at')

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code', 'district__name')
    list_filter = ('district', 'created_at', 'updated_at')

@admin.register(SubCounty)
class SubCountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'county', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code', 'county__name')
    list_filter = ('county', 'created_at', 'updated_at')

@admin.register(Parish)
class ParishAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcounty', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code', 'subcounty__name')
    list_filter = ('subcounty', 'created_at', 'updated_at')

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'parish', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code', 'parish__name')
    list_filter = ('parish', 'created_at', 'updated_at')

@admin.register(PaymentMode)
class PaymentModeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code', 'description')
    list_filter = ('created_at', 'updated_at')

@admin.register(Cooperative)
class CooperativeAdmin(admin.ModelAdmin):
    list_display = ('fpo_name', 'fpo_type', 'district', 'sub_county', 'contact_person', 'phone_number', 'registration_date')
    search_fields = ('fpo_name', 'contact_person', 'phone_number')
    list_filter = ('district', 'sub_county', 'registration_date')

@admin.register(FarmerGroup)
class FarmerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'cooperative', 'district', 'sub_county', 'village', 'contact_person', 'phone_number')
    list_filter = ('cooperative', 'district', 'sub_county', 'village')
    search_fields = ('name', 'code', 'contact_person', 'phone_number')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_id', 'gender', 'phone_number', 'role', 'district', 'sub_county', 'cooperative', 'farmer_group')
    list_filter = ('gender', 'role', 'cooperative', 'farmer_group', 'district', 'sub_county')
    search_fields = ('name', 'member_id', 'phone_number')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'get_current_price', 'created_at')
    list_filter = ('unit', 'created_at')
    search_fields = ('name', 'cooperative__fpo_name')
    date_hierarchy = 'created_at'

    def get_current_price(self, obj):
        current_price = obj.prices.first()
        if current_price:
            return f"{current_price.price} per {current_price.unit}"
        return "No price set"
    get_current_price.short_description = 'Current Price'
    
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('product','price','unit','effective_date') 
    list_filter=('product','effective_date')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'symbol', 'description')
    date_hierarchy = 'created_at'
