from rest_framework import serializers
from ..models import (
    Unit, Product, Price, District, County, SubCounty, Parish, Village, PaymentMode, Cooperative, FarmerGroup, Member, SupplierProduct, PlantingAllocation, Collection, LoanSupplier, CreditManager, Loan, Offtaker, Sale, Store, ThematicArea, Training
)

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
        depth = 1

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'
        depth = 1

class SubCountySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCounty
        fields = '__all__'
        depth = 1

class ParishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parish
        fields = '__all__'
        depth = 1

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'
        depth = 1

class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = '__all__'

class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = '__all__'
        depth = 1

class FarmerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerGroup
        fields = '__all__'
        depth = 1

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        depth = 1

class SupplierProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierProduct
        fields = '__all__'
        depth = 1

class PlantingAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantingAllocation
        fields = '__all__'
        depth = 1

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
        depth = 1

class LoanSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanSupplier
        fields = '__all__'

class CreditManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditManager
        fields = '__all__'
        depth = 1

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        depth = 1

class OfftakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offtaker
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
        depth = 1

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        depth = 1

class ThematicAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicArea
        fields = '__all__'

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'
        depth = 1


