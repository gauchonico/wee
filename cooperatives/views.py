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
    FarmerGroupBulkUploadForm, MemberBulkUploadForm
)
from .mixins import CustomLoginRequiredMixin
import csv
import io
from datetime import datetime
from django.db.models import Q
from django.views.generic.edit import FormView

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

    def generate_unique_code(self, base_code):
        """Generate a unique code by appending a number if the code already exists."""
        counter = 1
        new_code = base_code
        while Parish.objects.filter(code=new_code).exists():
            new_code = f"{base_code}{counter}"
            counter += 1
        return new_code

    def post(self, request):
        form = ParishBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            skipped_count = 0
            errors = []
            skipped_parishes = []

            # Get the header row to check column names
            headers = reader.fieldnames
            subcounty_column = None
            for possible_name in ['subcounty', 'sub_county', 'subcounty_name', 'sub_county_name']:
                if possible_name in headers:
                    subcounty_column = possible_name
                    break

            if not subcounty_column:
                messages.error(request, "CSV file must contain a column for subcounty (subcounty, sub_county, subcounty_name, or sub_county_name)")
                return render(request, self.template_name, {'form': form})

            for row in reader:
                try:
                    # Check if parish with this name already exists
                    if Parish.objects.filter(name=row['name']).exists():
                        skipped_parishes.append(row['name'])
                        skipped_count += 1
                        continue

                    # Get the subcounty using the correct column name
                    subcounty_name = row[subcounty_column]
                    try:
                        subcounty = SubCounty.objects.get(name=subcounty_name)
                    except SubCounty.DoesNotExist:
                        errors.append(f"Subcounty '{subcounty_name}' does not exist for parish '{row['name']}'")
                        error_count += 1
                        continue
                    
                    # Generate a unique code if the code already exists
                    original_code = row['code']
                    unique_code = self.generate_unique_code(original_code)
                    
                    # Create the parish with the unique code
                    Parish.objects.create(
                        name=row['name'],
                        code=unique_code,
                        subcounty=subcounty
                    )
                    success_count += 1
                except KeyError as e:
                    errors.append(f"Missing required column: {str(e)}")
                    error_count += 1
                except Exception as e:
                    errors.append(f"Error processing parish '{row.get('name', 'unknown')}': {str(e)}")
                    error_count += 1

            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} parishes.')
            if skipped_count > 0:
                messages.warning(request, f'Skipped {skipped_count} existing parishes: {", ".join(skipped_parishes)}')
            if error_count > 0:
                messages.error(request, f'Failed to import {error_count} parishes. See errors below.')
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

    def generate_unique_code(self, base_code):
        """Generate a unique code by appending a number if the code already exists."""
        counter = 1
        new_code = base_code
        while Village.objects.filter(code=new_code).exists():
            new_code = f"{base_code}{counter}"
            counter += 1
        return new_code

    def post(self, request):
        form = VillageBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            skipped_count = 0
            errors = []
            skipped_villages = []

            # Get the header row to check column names
            headers = reader.fieldnames
            parish_column = None
            for possible_name in ['parish', 'parish_name']:
                if possible_name in headers:
                    parish_column = possible_name
                    break

            if not parish_column:
                messages.error(request, "CSV file must contain a column for parish (parish or parish_name)")
                return render(request, self.template_name, {'form': form})

            for row in reader:
                try:
                    # Check if village with this name already exists
                    if Village.objects.filter(name=row['name']).exists():
                        skipped_villages.append(row['name'])
                        skipped_count += 1
                        continue

                    # Get the parish using the correct column name
                    parish_name = row[parish_column]
                    try:
                        parish = Parish.objects.get(name=parish_name)
                    except Parish.DoesNotExist:
                        errors.append(f"Parish '{parish_name}' does not exist for village '{row['name']}'")
                        error_count += 1
                        continue
                    
                    # Generate a unique code if the code already exists
                    original_code = row['code']
                    unique_code = self.generate_unique_code(original_code)
                    
                    # Create the village with the unique code
                    Village.objects.create(
                        name=row['name'],
                        code=unique_code,
                        parish=parish
                    )
                    success_count += 1
                except KeyError as e:
                    errors.append(f"Missing required column: {str(e)}")
                    error_count += 1
                except Exception as e:
                    errors.append(f"Error processing village '{row.get('name', 'unknown')}': {str(e)}")
                    error_count += 1

            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} villages.')
            if skipped_count > 0:
                messages.warning(request, f'Skipped {skipped_count} existing villages: {", ".join(skipped_villages)}')
            if error_count > 0:
                messages.error(request, f'Failed to import {error_count} villages. See errors below.')
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
    paginate_by = 50  # Show 50 farmer groups per page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(code__icontains=search_query) |
                Q(cooperative__fpo_name__icontains=search_query) |
                Q(district__name__icontains=search_query) |
                Q(sub_county__name__icontains=search_query) |
                Q(parish__name__icontains=search_query) |
                Q(village__name__icontains=search_query) |
                Q(contact_person__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )
        
        return queryset.select_related(
            'cooperative',
            'district',
            'sub_county',
            'parish',
            'village'
        ).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

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
    paginate_by = 50  # Show 50 members per page
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        # Add select_related for foreign key relationships to avoid N+1 queries
        queryset = queryset.select_related(
            'cooperative',
            'farmer_group',
            'district',
            'county',
            'sub_county',
            'village',
            'created_by'
        )
        
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(surname__icontains=search_query) |
                Q(other_name__icontains=search_query) |
                Q(member_id__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(cooperative__fpo_name__icontains=search_query) |
                Q(farmer_group__name__icontains=search_query)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

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

    def generate_unique_code(self, base_code):
        """Generate a unique code by appending a number if the code already exists."""
        counter = 1
        new_code = base_code
        while FarmerGroup.objects.filter(code=new_code).exists():
            new_code = f"{base_code}{counter}"
            counter += 1
        return new_code

    def post(self, request):
        form = FarmerGroupBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            error_count = 0
            skipped_count = 0
            errors = []
            skipped_groups = []

            for row in reader:
                try:
                    # Validate required fields
                    if not row.get('name'):
                        errors.append(f"Missing name for farmer group")
                        error_count += 1
                        continue
                    
                    if not row.get('cooperative'):
                        errors.append(f"Missing cooperative for farmer group '{row['name']}'")
                        error_count += 1
                        continue

                    # Check if farmer group with this name already exists
                    if FarmerGroup.objects.filter(name=row['name']).exists():
                        skipped_groups.append(row['name'])
                        skipped_count += 1
                        continue

                    # Get the cooperative
                    try:
                        cooperative = Cooperative.objects.get(fpo_name=row['cooperative'].strip())
                    except Cooperative.DoesNotExist:
                        errors.append(f"Cooperative '{row['cooperative']}' does not exist for farmer group '{row['name']}'")
                        error_count += 1
                        continue
                    
                    # Get the district
                    try:
                        district = District.objects.get(name=row['district'].strip())
                    except District.DoesNotExist:
                        errors.append(f"District '{row['district']}' does not exist for farmer group '{row['name']}'")
                        error_count += 1
                        continue
                    
                    # Get the sub-county
                    try:
                        sub_county = SubCounty.objects.get(name=row['sub_county'].strip())
                    except SubCounty.DoesNotExist:
                        errors.append(f"Sub-county '{row['sub_county']}' does not exist for farmer group '{row['name']}'")
                        error_count += 1
                        continue
                    
                    # Get the parish if provided
                    parish = None
                    if row.get('parish'):
                        try:
                            # Get the first parish that matches the name and belongs to the correct sub-county
                            parish = Parish.objects.filter(
                                name=row['parish'].strip(),
                                subcounty=sub_county
                            ).first()
                            
                            if not parish:
                                errors.append(f"Parish '{row['parish']}' does not exist in sub-county '{sub_county.name}' for farmer group '{row['name']}'")
                                error_count += 1
                                continue
                        except Exception as e:
                            errors.append(f"Error finding parish '{row['parish']}' for farmer group '{row['name']}': {str(e)}")
                            error_count += 1
                            continue
                    
                    # Get the village if provided
                    village = None
                    if row.get('village'):
                        try:
                            # Get the first village that matches the name and belongs to the correct parish
                            village = Village.objects.filter(
                                name=row['village'].strip(),
                                parish=parish
                            ).first() if parish else None
                            
                            if not village:
                                errors.append(f"Village '{row['village']}' does not exist in parish '{parish.name if parish else 'unknown'}' for farmer group '{row['name']}'")
                                error_count += 1
                                continue
                        except Exception as e:
                            errors.append(f"Error finding village '{row['village']}' for farmer group '{row['name']}': {str(e)}")
                            error_count += 1
                            continue
                    
                    # Generate a unique code if the code already exists
                    original_code = row['code']
                    unique_code = self.generate_unique_code(original_code)
                    
                    # Parse the created_at date if provided
                    created_at = None
                    if row.get('created_at'):
                        try:
                            # Try different date formats
                            date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']
                            for date_format in date_formats:
                                try:
                                    created_at = datetime.strptime(row['created_at'].strip(), date_format).date()
                                    break
                                except ValueError:
                                    continue
                            
                            if not created_at:
                                errors.append(f"Invalid date format for '{row['name']}'. Use YYYY-MM-DD, DD-MM-YYYY, or MM/DD/YYYY")
                                error_count += 1
                                continue
                        except Exception as e:
                            errors.append(f"Error parsing date for '{row['name']}': {str(e)}")
                            error_count += 1
                            continue
                    
                    # Create the farmer group
                    farmer_group = FarmerGroup.objects.create(
                        name=row['name'].strip(),
                        code=unique_code,
                        cooperative=cooperative,
                        district=district,
                        sub_county=sub_county,
                        parish=parish,
                        village=village,
                        contact_person=row['contact_person'].strip(),
                        phone_number=row['phone_number'].strip()
                    )
                    
                    # Set the created_at date if provided
                    if created_at:
                        farmer_group.created_at = created_at
                        farmer_group.save()
                    
                    success_count += 1
                except KeyError as e:
                    errors.append(f"Missing required column: {str(e)}")
                    error_count += 1
                except Exception as e:
                    errors.append(f"Error processing farmer group '{row.get('name', 'unknown')}': {str(e)}")
                    error_count += 1

            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} farmer groups.')
            if skipped_count > 0:
                messages.warning(request, f'Skipped {skipped_count} existing farmer groups: {", ".join(skipped_groups)}')
            if error_count > 0:
                messages.error(request, f'Failed to import {error_count} farmer groups. See errors below.')
                for error in errors:
                    messages.error(request, error)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

class MemberBulkUploadView(CustomLoginRequiredMixin, FormView):
    template_name = 'cooperatives/member_bulk_upload.html'
    form_class = MemberBulkUploadForm
    success_url = reverse_lazy('cooperatives:member-list')

    def form_valid(self, form):
        csv_file = form.cleaned_data['csv_file']
        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.DictReader(io.StringIO(decoded_file))
        
        success_count = 0
        error_count = 0
        error_messages = []

        for row in csv_data:
            try:
                # Validate gender
                gender = row.get('gender', '').upper()
                if gender not in ['M', 'F', 'O']:
                    raise ValueError(f"Invalid gender value '{gender}'. Must be 'M', 'F', or 'O'")

                # Parse date of birth if provided
                date_of_birth = None
                if row.get('date_of_birth'):
                    try:
                        # Try different date formats
                        date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y']
                        for date_format in date_formats:
                            try:
                                date_of_birth = datetime.strptime(row['date_of_birth'].strip(), date_format).date()
                                break
                            except ValueError:
                                continue
                        
                        if not date_of_birth:
                            raise ValueError(f"Invalid date format for date of birth. Use YYYY-MM-DD, DD-MM-YYYY, or MM/DD/YYYY")
                    except Exception as e:
                        raise ValueError(f"Error parsing date of birth: {str(e)}")

                # Get related objects
                cooperative = Cooperative.objects.get(fpo_name=row['cooperative_name'])
                district = District.objects.get(name=row['district'])
                county = County.objects.get(name=row['county'], district=district)
                sub_county = SubCounty.objects.get(name=row['subcounty'], county=county)
                village = Village.objects.get(name=row['village'])
                
                # Handle optional farmer group
                farmer_group = None
                if row.get('farmer_group_name'):
                    farmer_group = FarmerGroup.objects.get(
                        name=row['farmer_group_name'],
                        cooperative=cooperative
                    )

                # Handle products (comma-separated list)
                product_names = [name.strip() for name in row['products'].split(',')]
                products = Product.objects.filter(name__in=product_names)

                # Create member instance
                member = Member.objects.create(
                    member_id=row['userId'],
                    first_name=row['firstname'],
                    surname=row['surname'],
                    other_name=row.get('othername', ''),
                    date_of_birth=date_of_birth,
                    email=row.get('email', ''),
                    phone_number=row['phone_number'],
                    gender=gender,
                    id_number=row['id_number'],
                    cooperative=cooperative,
                    farmer_group=farmer_group,
                    district=district,
                    county=county,
                    sub_county=sub_county,
                    village=village,
                    gps_coordinates=row['gps_coordinates'],
                    role=row['role'].lower(),
                    land_acres=float(row['land_acreage'] or 0),
                    shea_trees=int(row['shea_trees'] or 0),
                    beehives=int(row['beehives'] or 0),
                    created_by=self.request.user
                )

                # Add products
                member.products.set(products)
                success_count += 1

            except (Cooperative.DoesNotExist, District.DoesNotExist,
                    County.DoesNotExist, SubCounty.DoesNotExist,
                    Village.DoesNotExist, FarmerGroup.DoesNotExist) as e:
                error_count += 1
                error_messages.append(f"Row {csv_data.line_num}: {str(e)}")
            except ValueError as e:
                error_count += 1
                error_messages.append(f"Row {csv_data.line_num}: {str(e)}")
            except Exception as e:
                error_count += 1
                error_messages.append(f"Row {csv_data.line_num}: {str(e)}")

        # Add messages for user feedback
        if success_count:
            messages.success(self.request, f"Successfully imported {success_count} members.")
        if error_count:
            messages.error(self.request, f"Failed to import {error_count} members.")
            for error in error_messages[:5]:  # Show first 5 errors
                messages.warning(self.request, error)
            if len(error_messages) > 5:
                messages.warning(self.request, f"... and {len(error_messages) - 5} more errors.")

        return super().form_valid(form)
