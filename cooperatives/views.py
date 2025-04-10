from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from .models import (
    District, County, SubCounty, Parish, Village, PaymentMode,
    Cooperative, FarmerGroup, Member, Product, Price, Unit
)
from .forms import (
    DistrictForm, CountyForm, SubCountyForm, ParishForm, VillageForm, PaymentModeForm,
    CooperativeForm, FarmerGroupForm, MemberForm, ProductForm, PriceForm, UnitForm, CooperativeBulkUploadForm,
    ParishBulkUploadForm, VillageBulkUploadForm, SubCountyBulkUploadForm, CountyBulkUploadForm, DistrictBulkUploadForm,
    FarmerGroupBulkUploadForm
)
from .mixins import CustomLoginRequiredMixin
import csv
import io
from datetime import datetime

# District Views
class DistrictListView(CustomLoginRequiredMixin, ListView):
    model = District
    template_name = 'cooperatives/district_list.html'
    context_object_name = 'districts'

class DistrictDetailView(CustomLoginRequiredMixin, DetailView):
    model = District
    template_name = 'cooperatives/district_detail.html'
    context_object_name = 'district'
    
class DistrictCreateView(CustomLoginRequiredMixin, CreateView):
    model = District
    form_class = DistrictForm
    template_name = 'cooperatives/district_form.html'
    success_url = reverse_lazy('cooperatives:district-list')

class DistrictUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = District
    form_class = DistrictForm
    template_name = 'cooperatives/district_form.html'
    success_url = reverse_lazy('cooperatives:district-list')

class DistrictDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = District
    template_name = 'cooperatives/district_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:district-list')

# County Views
class CountyListView(CustomLoginRequiredMixin, ListView):
    model = County
    template_name = 'cooperatives/county_list.html'
    context_object_name = 'counties'

class CountyDetailView(CustomLoginRequiredMixin, DetailView):
    model = County
    template_name = 'cooperatives/county_detail.html'
    context_object_name = 'county'

class CountyCreateView(CustomLoginRequiredMixin, CreateView):
    model = County
    form_class = CountyForm
    template_name = 'cooperatives/county_form.html'
    success_url = reverse_lazy('cooperatives:county-list')

class CountyUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = County
    form_class = CountyForm
    template_name = 'cooperatives/county_form.html'
    success_url = reverse_lazy('cooperatives:county-list')

class CountyDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = County
    template_name = 'cooperatives/county_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:county-list')

# SubCounty Views
class SubCountyListView(CustomLoginRequiredMixin, ListView):
    model = SubCounty
    template_name = 'cooperatives/subcounty_list.html'
    context_object_name = 'subcounties'

class SubCountyDetailView(CustomLoginRequiredMixin, DetailView):
    model = SubCounty
    template_name = 'cooperatives/subcounty_detail.html'
    context_object_name = 'subcounty'

class SubCountyCreateView(CustomLoginRequiredMixin, CreateView):
    model = SubCounty
    form_class = SubCountyForm
    template_name = 'cooperatives/subcounty_form.html'
    success_url = reverse_lazy('cooperatives:subcounty-list')

class SubCountyUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = SubCounty
    form_class = SubCountyForm
    template_name = 'cooperatives/subcounty_form.html'
    success_url = reverse_lazy('cooperatives:subcounty-list')

class SubCountyDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = SubCounty
    template_name = 'cooperatives/subcounty_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:subcounty-list')

# Parish Views
class ParishListView(CustomLoginRequiredMixin, ListView):
    model = Parish
    template_name = 'cooperatives/parish_list.html'
    context_object_name = 'parishes'

class ParishDetailView(CustomLoginRequiredMixin, DetailView):
    model = Parish
    template_name = 'cooperatives/parish_detail.html'
    context_object_name = 'parish'

class ParishCreateView(CustomLoginRequiredMixin, CreateView):
    model = Parish
    form_class = ParishForm
    template_name = 'cooperatives/parish_form.html'
    success_url = reverse_lazy('cooperatives:parish-list')

class ParishUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Parish
    form_class = ParishForm
    template_name = 'cooperatives/parish_form.html'
    success_url = reverse_lazy('cooperatives:parish-list')

class ParishDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Parish
    template_name = 'cooperatives/parish_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:parish-list')

class ParishBulkUploadView(CustomLoginRequiredMixin, View):
    template_name = 'cooperatives/parish_bulk_upload.html'
    success_url = reverse_lazy('cooperatives:parish-list')

    def get(self, request):
        form = ParishBulkUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ParishBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            errors = []

            for row in reader:
                try:
                    # Get the subcounty
                    subcounty = SubCounty.objects.get(name=row['subcounty'])
                    
                    # Create the parish
                    Parish.objects.create(
                        name=row['name'],
                        code=row['code'],
                        subcounty=subcounty
                    )
                    success_count += 1
                except SubCounty.DoesNotExist:
                    error_count += 1
                    errors.append(f"Sub county '{row['subcounty']}' not found for parish '{row['name']}'")
                except Exception as e:
                    error_count += 1
                    errors.append(f"Error creating parish '{row['name']}': {str(e)}")

            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} parishes.')
            if error_count > 0:
                messages.warning(request, f'Failed to import {error_count} parishes.')
                for error in errors:
                    messages.error(request, error)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

# Village Views
class VillageListView(CustomLoginRequiredMixin, ListView):
    model = Village
    template_name = 'cooperatives/village_list.html'
    context_object_name = 'villages'

class VillageDetailView(CustomLoginRequiredMixin, DetailView):
    model = Village
    template_name = 'cooperatives/village_detail.html'
    context_object_name = 'village'

class VillageCreateView(CustomLoginRequiredMixin, CreateView):
    model = Village
    form_class = VillageForm
    template_name = 'cooperatives/village_form.html'
    success_url = reverse_lazy('cooperatives:village-list')

class VillageUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Village
    form_class = VillageForm
    template_name = 'cooperatives/village_form.html'
    success_url = reverse_lazy('cooperatives:village-list')

class VillageDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Village
    template_name = 'cooperatives/village_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:village-list')

class VillageBulkUploadView(CustomLoginRequiredMixin, View):
    template_name = 'cooperatives/village_bulk_upload.html'
    success_url = reverse_lazy('cooperatives:village-list')

    def get(self, request):
        form = VillageBulkUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = VillageBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            errors = []

            for row in reader:
                try:
                    # Get the parish
                    parish = Parish.objects.get(name=row['parish'])
                    
                    # Create the village
                    Village.objects.create(
                        name=row['name'],
                        code=row['code'],
                        parish=parish
                    )
                    success_count += 1
                except Parish.DoesNotExist:
                    error_count += 1
                    errors.append(f"Parish '{row['parish']}' not found for village '{row['name']}'")
                except Exception as e:
                    error_count += 1
                    errors.append(f"Error creating village '{row['name']}': {str(e)}")

            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} villages.')
            if error_count > 0:
                messages.warning(request, f'Failed to import {error_count} villages.')
                for error in errors:
                    messages.error(request, error)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

# PaymentMode Views
class PaymentModeListView(CustomLoginRequiredMixin, ListView):
    model = PaymentMode
    template_name = 'cooperatives/paymentmode_list.html'
    context_object_name = 'paymentmodes'

class PaymentModeDetailView(CustomLoginRequiredMixin, DetailView):
    model = PaymentMode
    template_name = 'cooperatives/paymentmode_detail.html'
    context_object_name = 'paymentmode'

class PaymentModeCreateView(CustomLoginRequiredMixin, CreateView):
    model = PaymentMode
    form_class = PaymentModeForm
    template_name = 'cooperatives/paymentmode_form.html'
    success_url = reverse_lazy('cooperatives:paymentmode-list')

class PaymentModeUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = PaymentMode
    form_class = PaymentModeForm
    template_name = 'cooperatives/paymentmode_form.html'
    success_url = reverse_lazy('cooperatives:paymentmode-list')

class PaymentModeDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = PaymentMode
    template_name = 'cooperatives/paymentmode_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:paymentmode-list')

# Cooperative Views
class CooperativeListView(CustomLoginRequiredMixin, ListView):
    model = Cooperative
    template_name = 'cooperatives/cooperative_list.html'
    context_object_name = 'cooperatives'

class CooperativeDetailView(CustomLoginRequiredMixin, DetailView):
    model = Cooperative
    template_name = 'cooperatives/cooperative_detail.html'
    context_object_name = 'cooperative'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmer_groups'] = self.object.farmer_groups.all()
        return context

class CooperativeCreateView(CustomLoginRequiredMixin, CreateView):
    model = Cooperative
    form_class = CooperativeForm
    template_name = 'cooperatives/cooperative_form.html'
    success_url = reverse_lazy('cooperatives:cooperative-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Cooperative created successfully.')
        return super().form_valid(form)

class CooperativeUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cooperative
    form_class = CooperativeForm
    template_name = 'cooperatives/cooperative_form.html'
    success_url = reverse_lazy('cooperatives:cooperative-list')
    
    def test_func(self):
        cooperative = self.get_object()
        return self.request.user.is_staff or self.request.user == cooperative.created_by
    
    def form_valid(self, form):
        messages.success(self.request, 'Cooperative updated successfully.')
        return super().form_valid(form)

class CooperativeDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cooperative
    template_name = 'cooperatives/cooperative_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:cooperative-list')
    
    def test_func(self):
        cooperative = self.get_object()
        return self.request.user.is_staff or self.request.user == cooperative.created_by
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cooperative deleted successfully.')
        return super().delete(request, *args, **kwargs)

# FarmerGroup Views
class FarmerGroupListView(CustomLoginRequiredMixin, ListView):
    model = FarmerGroup
    template_name = 'cooperatives/farmer_group_list.html'
    context_object_name = 'farmer_groups'

class FarmerGroupDetailView(CustomLoginRequiredMixin, DetailView):
    model = FarmerGroup
    template_name = 'cooperatives/farmer_group_detail.html'
    context_object_name = 'farmer_group'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.group_members.all()
        return context

class FarmerGroupCreateView(CustomLoginRequiredMixin, CreateView):
    model = FarmerGroup
    form_class = FarmerGroupForm
    template_name = 'cooperatives/farmer_group_form.html'
    success_url = reverse_lazy('cooperatives:farmer-group-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Farmer Group created successfully.')
        return super().form_valid(form)

class FarmerGroupUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FarmerGroup
    form_class = FarmerGroupForm
    template_name = 'cooperatives/farmer_group_form.html'
    success_url = reverse_lazy('cooperatives:farmer-group-list')
    
    def test_func(self):
        farmer_group = self.get_object()
        return self.request.user.is_staff or self.request.user == farmer_group.created_by
    
    def form_valid(self, form):
        messages.success(self.request, 'Farmer Group updated successfully.')
        return super().form_valid(form)

class FarmerGroupDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FarmerGroup
    template_name = 'cooperatives/farmer_group_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:farmer-group-list')
    
    def test_func(self):
        farmer_group = self.get_object()
        return self.request.user.is_staff or self.request.user == farmer_group.created_by
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Farmer Group deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Member Views
class MemberListView(CustomLoginRequiredMixin, ListView):
    model = Member
    template_name = 'cooperatives/member_list.html'
    context_object_name = 'members'

class MemberDetailView(CustomLoginRequiredMixin, DetailView):
    model = Member
    template_name = 'cooperatives/member_detail.html'
    context_object_name = 'member'

class MemberCreateView(CustomLoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'cooperatives/member_form.html'
    success_url = reverse_lazy('cooperatives:member-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Member created successfully.')
        return super().form_valid(form)

class MemberUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'cooperatives/member_form.html'
    success_url = reverse_lazy('cooperatives:member-list')
    
    def test_func(self):
        member = self.get_object()
        return self.request.user.is_staff or self.request.user == member.created_by
    
    def form_valid(self, form):
        messages.success(self.request, 'Member updated successfully.')
        return super().form_valid(form)

class MemberDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Member
    template_name = 'cooperatives/member_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:member-list')
    
    def test_func(self):
        member = self.get_object()
        return self.request.user.is_staff or self.request.user == member.created_by
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Member deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Product Views
class ProductListView(CustomLoginRequiredMixin, ListView):
    model = Product
    template_name = 'cooperatives/product_list.html'
    context_object_name = 'products'

class ProductDetailView(CustomLoginRequiredMixin, DetailView):
    model = Product
    template_name = 'cooperatives/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prices'] = self.object.prices.all()
        return context

class ProductCreateView(CustomLoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'cooperatives/product_form.html'
    success_url = reverse_lazy('cooperatives:product-list')
    
    def form_valid(self, form):
        # Get the user's member record and set the cooperative
        member = Member.objects.filter(created_by=self.request.user).first()
        if member:
            form.instance.cooperative = member.cooperative
            form.instance.created_by = self.request.user
            messages.success(self.request, 'Product created successfully.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'You must be a member to create products.')
            return self.form_invalid(form)

class ProductUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'cooperatives/product_form.html'
    success_url = reverse_lazy('cooperatives:product-list')
    
    def test_func(self):
        product = self.get_object()
        return self.request.user.is_staff or self.request.user == product.created_by
    
    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully.')
        return super().form_valid(form)

class ProductDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'cooperatives/product_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:product-list')
    
    def test_func(self):
        product = self.get_object()
        return self.request.user.is_staff or self.request.user == product.created_by
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Price Views
class PriceListView(CustomLoginRequiredMixin, ListView):
    model = Price
    template_name = 'cooperatives/price_list.html'
    context_object_name = 'prices'

class PriceDetailView(CustomLoginRequiredMixin, DetailView):
    model = Price
    template_name = 'cooperatives/price_detail.html'
    context_object_name = 'price'

class PriceCreateView(CustomLoginRequiredMixin, CreateView):
    model = Price
    form_class = PriceForm
    template_name = 'cooperatives/price_form.html'
    success_url = reverse_lazy('cooperatives:price-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Price created successfully.')
        return super().form_valid(form)

class PriceUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Price
    form_class = PriceForm
    template_name = 'cooperatives/price_form.html'
    success_url = reverse_lazy('cooperatives:price-list')
    
    def test_func(self):
        price = self.get_object()
        return self.request.user.is_staff or self.request.user == price.created_by
    
    def form_valid(self, form):
        messages.success(self.request, 'Price updated successfully.')
        return super().form_valid(form)

class PriceDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Price
    template_name = 'cooperatives/price_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:price-list')
    
    def test_func(self):
        price = self.get_object()
        return self.request.user.is_staff or self.request.user == price.created_by
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Price deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Unit Views
class UnitListView(CustomLoginRequiredMixin, ListView):
    model = Unit
    template_name = 'cooperatives/unit_list.html'
    context_object_name = 'units'

class UnitDetailView(CustomLoginRequiredMixin, DetailView):
    model = Unit
    template_name = 'cooperatives/unit_detail.html'
    context_object_name = 'unit'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.all()
        return context

class UnitCreateView(CustomLoginRequiredMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'cooperatives/unit_form.html'
    success_url = reverse_lazy('cooperatives:unit-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Unit created successfully.')
        return super().form_valid(form)

class UnitUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'cooperatives/unit_form.html'
    success_url = reverse_lazy('cooperatives:unit-list')
    
    def test_func(self):
        unit = self.get_object()
        return self.request.user.is_staff or self.request.user == unit.created_by
    
    def form_valid(self, form):
        messages.success(self.request, 'Unit updated successfully.')
        return super().form_valid(form)

class UnitDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Unit
    template_name = 'cooperatives/unit_confirm_delete.html'
    success_url = reverse_lazy('cooperatives:unit-list')
    
    def test_func(self):
        unit = self.get_object()
        return self.request.user.is_staff or self.request.user == unit.created_by
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Unit deleted successfully.')
        return super().delete(request, *args, **kwargs)

class CooperativeBulkUploadView(CustomLoginRequiredMixin, View):
    template_name = 'cooperatives/cooperative_bulk_upload.html'
    success_url = reverse_lazy('cooperatives:cooperative-list')
    
    def get(self, request):
        form = CooperativeBulkUploadForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CooperativeBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            errors = []
            
            for row in reader:
                try:
                    # Get district and sub_county objects
                    district = District.objects.filter(name=row['district']).first()
                    sub_county = SubCounty.objects.filter(name=row['sub_county']).first()
                    
                    if not district or not sub_county:
                        error_count += 1
                        errors.append(f"Row {reader.line_num}: District or Sub County not found")
                        continue
                    
                    # Parse the created_at date if provided
                    created_at = None
                    if 'registration_date' in row and row['registration_date']:
                        try:
                            created_at = datetime.strptime(row['registration_date'], '%Y-%m-%d').date()
                        except ValueError:
                            error_count += 1
                            errors.append(f"Row {reader.line_num}: Invalid date format. Use YYYY-MM-DD")
                            continue
                    
                    # Create cooperative
                    cooperative = Cooperative.objects.create(
                        fpo_name=row['fpo_name'],
                        fpo_type=row['fpo_type'],
                        district=district,
                        sub_county=sub_county,
                        contact_person=row['contact_person'],
                        phone_number=row['phone_number'],
            
                    )
                    
                    # Update created_at if provided
                    if created_at:
                        cooperative.registration_date = created_at
                        cooperative.save()
                    
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"Row {reader.line_num}: {str(e)}")
            
            if success_count > 0:
                messages.success(request, f"Successfully imported {success_count} cooperatives.")
            if error_count > 0:
                messages.warning(request, f"Failed to import {error_count} cooperatives. See details below.")
                for error in errors:
                    messages.error(request, error)
            
            return redirect(self.success_url)
        
        return render(request, self.template_name, {'form': form})

class SubCountyBulkUploadView(CustomLoginRequiredMixin, View):
    template_name = 'cooperatives/subcounty_bulk_upload.html'
    success_url = reverse_lazy('cooperatives:subcounty-list')

    def get(self, request):
        form = SubCountyBulkUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SubCountyBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            errors = []

            for row in reader:
                try:
                    # Get the county
                    county = County.objects.get(name=row['county'])
                    
                    # Create the subcounty
                    SubCounty.objects.create(
                        name=row['name'],
                        code=row['code'],
                        county=county
                    )
                    success_count += 1
                except County.DoesNotExist:
                    error_count += 1
                    errors.append(f"County '{row['county']}' not found for sub county '{row['name']}'")
                except Exception as e:
                    error_count += 1
                    errors.append(f"Error creating sub county '{row['name']}': {str(e)}")

            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} sub counties.')
            if error_count > 0:
                messages.warning(request, f'Failed to import {error_count} sub counties.')
                for error in errors:
                    messages.error(request, error)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

class CountyBulkUploadView(CustomLoginRequiredMixin, View):
    template_name = 'cooperatives/county_bulk_upload.html'
    success_url = reverse_lazy('cooperatives:county-list')

    def get(self, request):
        form = CountyBulkUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CountyBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            errors = []

            for row in reader:
                try:
                    # Get the district
                    district = District.objects.get(name=row['district'])
                    
                    # Create the county
                    County.objects.create(
                        name=row['name'],
                        code=row['code'],
                        district=district
                    )
                    success_count += 1
                except District.DoesNotExist:
                    error_count += 1
                    errors.append(f"District '{row['district']}' not found for county '{row['name']}'")
                except Exception as e:
                    error_count += 1
                    errors.append(f"Error creating county '{row['name']}': {str(e)}")

            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} counties.')
            if error_count > 0:
                messages.warning(request, f'Failed to import {error_count} counties.')
                for error in errors:
                    messages.error(request, error)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

class DistrictBulkUploadView(CustomLoginRequiredMixin, View):
    template_name = 'cooperatives/district_bulk_upload.html'
    success_url = reverse_lazy('cooperatives:district-list')

    def get(self, request):
        form = DistrictBulkUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = DistrictBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            errors = []

            for row in reader:
                try:
                    # Create the district
                    District.objects.create(
                        name=row['name'],
                        code=row['code']
                    )
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"Error creating district '{row['name']}': {str(e)}")

            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} districts.')
            if error_count > 0:
                messages.warning(request, f'Failed to import {error_count} districts.')
                for error in errors:
                    messages.error(request, error)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

class FarmerGroupBulkUploadView(CustomLoginRequiredMixin, View):
    template_name = 'cooperatives/farmer_group_bulk_upload.html'
    success_url = reverse_lazy('cooperatives:farmer-group-list')

    def get(self, request):
        form = FarmerGroupBulkUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FarmerGroupBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            errors = []

            for row in reader:
                try:
                    # Get the cooperative
                    cooperative = Cooperative.objects.get(fpo_name=row['cooperative'])
                    
                    # Get the district
                    district = District.objects.get(name=row['district'])
                    
                    # Get the sub-county
                    sub_county = SubCounty.objects.get(name=row['sub_county'])
                    
                    # Get the parish if provided
                    parish = None
                    if row.get('parish'):
                        parish = Parish.objects.get(name=row['parish'])
                    
                    # Get the product if provided
                    product = None
                    if row.get('product'):
                        product = Product.objects.get(name=row['product'])
                    
                    # Parse boolean fields
                    is_VSLA = row.get('is_VSLA', '').lower() in ('true', 'yes', '1')
                    is_active = row.get('is_active', '').lower() not in ('false', 'no', '0')
                    
                    # Create the farmer group
                    FarmerGroup.objects.create(
                        name=row['name'],
                        code=row['code'],
                        cooperative=cooperative,
                        district=district,
                        sub_county=sub_county,
                        parish=parish,
                        village=row.get('village'),
                        contact_person=row['contact_person'],
                        phone_number=row['phone_number'],
                        product=product,
                        is_VSLA=is_VSLA,
                        is_active=is_active
                    )
                    success_count += 1
                except Cooperative.DoesNotExist:
                    error_count += 1
                    errors.append(f"Cooperative '{row['cooperative']}' not found for farmer group '{row['name']}'")
                except District.DoesNotExist:
                    error_count += 1
                    errors.append(f"District '{row['district']}' not found for farmer group '{row['name']}'")
                except SubCounty.DoesNotExist:
                    error_count += 1
                    errors.append(f"Sub-county '{row['sub_county']}' not found for farmer group '{row['name']}'")
                except Exception as e:
                    error_count += 1
                    errors.append(f"Error creating farmer group '{row['name']}': {str(e)}")

            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} farmer groups.')
            if error_count > 0:
                messages.warning(request, f'Failed to import {error_count} farmer groups.')
                for error in errors:
                    messages.error(request, error)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
