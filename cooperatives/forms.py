from django import forms
from .models import (
    District, County, SubCounty, Parish, Village, PaymentMode,
    Cooperative, FarmerGroup, Member, Product, Price, Unit
)

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CountyForm(forms.ModelForm):
    class Meta:
        model = County
        fields = ['name', 'district', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SubCountyForm(forms.ModelForm):
    class Meta:
        model = SubCounty
        fields = ['name', 'county', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'county': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ParishForm(forms.ModelForm):
    class Meta:
        model = Parish
        fields = ['name', 'subcounty', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subcounty': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ['name', 'parish', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parish': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Village.objects.filter(code=code).exists():
            raise forms.ValidationError("A village with this code already exists.")
        return code

class PaymentModeForm(forms.ModelForm):
    class Meta:
        model = PaymentMode
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CooperativeForm(forms.ModelForm):
    class Meta:
        model = Cooperative
        fields = ['logo', 'fpo_name', 'fpo_type', 'product', 'district', 'sub_county', 'contact_person', 'phone_number']
        widgets = {
            'fpo_name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class':'form-control'}),
            'fpo_type': forms.Select(attrs={'class':'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'sub_county': forms.Select(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number


class FarmerGroupForm(forms.ModelForm):
    class Meta:
        model = FarmerGroup
        fields = ['name', 'code', 'cooperative', 'district', 'sub_county', 'parish', 'village', 'contact_person', 'phone_number', 'product', 'is_VSLA', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'cooperative': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'sub_county': forms.Select(attrs={'class': 'form-control'}),
            'parish': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.Select(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'is_VSLA': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
            
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if FarmerGroup.objects.filter(code=code).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("This code is already in use.")
        return code


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name', 'surname', 'other_name', 'member_id', 'email',
            'phone_number', 'gender', 'role', 'district', 'county',
            'sub_county', 'village', 'cooperative', 'farmer_group',
            'gps_coordinates', 'id_type', 'id_number', 'is_verified',
            'has_mobile_money', 'is_refugee', 'land_acres', 'shea_trees',
            'beehives', 'products'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'other_name': forms.TextInput(attrs={'class': 'form-control'}),
            'member_id': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'county': forms.Select(attrs={'class': 'form-control'}),
            'sub_county': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.Select(attrs={'class': 'form-control'}),
            'cooperative': forms.Select(attrs={'class': 'form-control'}),
            'farmer_group': forms.Select(attrs={'class': 'form-control'}),
            'gps_coordinates': forms.TextInput(attrs={'class': 'form-control'}),
            'id_type': forms.Select(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_mobile_money': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_refugee': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'land_acres': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'shea_trees': forms.NumberInput(attrs={'class': 'form-control'}),
            'beehives': forms.NumberInput(attrs={'class': 'form-control'}),
            'products': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter farmer groups based on selected cooperative
        if 'cooperative' in self.data:
            try:
                cooperative_id = int(self.data.get('cooperative'))
                self.fields['farmer_group'].queryset = FarmerGroup.objects.filter(cooperative_id=cooperative_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['farmer_group'].queryset = self.instance.cooperative.farmer_groups.all()
        else:
            self.fields['farmer_group'].queryset = FarmerGroup.objects.none()
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number
    
    def clean_member_id(self):
        member_id = self.cleaned_data.get('member_id')
        if Member.objects.filter(member_id=member_id).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("This member ID is already in use.")
        return member_id

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'symbol', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'symbol': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
        }

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['product', 'price', 'unit', 'effective_date']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CooperativeBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with cooperative data. Required columns: fpo_name, fpo_type, district, sub_county, contact_person, phone_number',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )

class ParishBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: name, code, subcounty',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

class VillageBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: name, code, parish',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

class SubCountyBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: name, code, county',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

class CountyBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: name, code, district',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

class DistrictBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: name, code',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

class FarmerGroupBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with the following columns: name, code, cooperative, district, sub_county, parish, village, contact_person, phone_number, product, is_VSLA, is_active',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

class MemberBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Select CSV File',
        help_text='Upload a CSV file containing member information.',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV document.')
        return csv_file 