from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib import messages
from .models import Agent, District
from .forms import AgentForm, AgentBulkUploadForm
from cooperatives.mixins import CustomLoginRequiredMixin
from django.db.models import Q
import csv
import io
from datetime import datetime

# Create your views here.

class AgentListView(CustomLoginRequiredMixin, ListView):
    model = Agent
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'
    paginate_by = 50  # Show 50 agents per page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(agent_id__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )
        
        return queryset.prefetch_related('districts', 'farmer_groups').order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class AgentDetailView(CustomLoginRequiredMixin, DetailView):
    model = Agent
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

class AgentCreateView(CustomLoginRequiredMixin, CreateView):
    model = Agent
    form_class = AgentForm
    template_name = 'agents/agent_form.html'
    success_url = reverse_lazy('agents:agent-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Agent created successfully.')
        return super().form_valid(form)

class AgentUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Agent
    form_class = AgentForm
    template_name = 'agents/agent_form.html'
    success_url = reverse_lazy('agents:agent-list')
    
    def test_func(self):
        agent = self.get_object()
        return self.request.user.is_staff or self.request.user == agent.created_by
    
    def form_valid(self, form):
        messages.success(self.request, 'Agent updated successfully.')
        return super().form_valid(form)

class AgentDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Agent
    template_name = 'agents/agent_confirm_delete.html'
    success_url = reverse_lazy('agents:agent-list')
    
    def test_func(self):
        agent = self.get_object()
        return self.request.user.is_staff or self.request.user == agent.created_by
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Agent deleted successfully.')
        return super().delete(request, *args, **kwargs)

class AgentBulkUploadView(LoginRequiredMixin, FormView):
    template_name = 'agents/agent_bulk_upload.html'
    form_class = AgentBulkUploadForm
    success_url = reverse_lazy('agents:agent-list')

    def form_valid(self, form):
        csv_file = form.cleaned_data['csv_file']
        file_content = csv_file.read()
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        decoded_content = None
        
        for encoding in encodings:
            try:
                decoded_content = file_content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if decoded_content is None:
            messages.error(self.request, 'Could not decode the file. Please ensure it is saved in UTF-8, Latin-1, or Windows-1252 encoding.')
            return self.form_invalid(form)
        
        io_string = io.StringIO(decoded_content)
        reader = csv.DictReader(io_string)
        
        success_count = 0
        error_count = 0
        update_count = 0
        errors = []

        for row in reader:
            try:
                # Parse districts - handle empty values
                district_names = []
                if row.get('districts'):
                    district_names = [d.strip() for d in row['districts'].split(',') if d.strip()]
                
                districts = []
                for name in district_names:
                    district = District.objects.filter(name__iexact=name).first()
                    if district:
                        districts.append(district)
                    else:
                        errors.append(f"District '{name}' not found for agent {row.get('agent_id', 'Unknown')}")

                # Create agent with only the fields that exist in the CSV
                agent_data = {
                    'agent_id': row['agent_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'phone_number': row['phone_number'],
                    'gender': row['gender'],
                    'is_active': True,
                    'date_of_birth': datetime(1990, 1, 1).date()  # Default date of birth
                }

                # Add optional fields if they exist
                if row.get('date_joined'):
                    try:
                        agent_data['date_joined'] = datetime.strptime(row['date_joined'], '%Y-%m-%d').date()
                    except ValueError:
                        errors.append(f"Invalid date format for date_joined in agent {row['agent_id']}")
                        continue

                if row.get('farmers_profiled'):
                    try:
                        agent_data['farmers_profiled'] = int(row['farmers_profiled'])
                    except ValueError:
                        agent_data['farmers_profiled'] = 0

                # Check if agent with this email already exists
                existing_agent = Agent.objects.filter(email=row['email']).first()
                if existing_agent:
                    # Update existing agent
                    for key, value in agent_data.items():
                        setattr(existing_agent, key, value)
                    existing_agent.save()
                    if districts:
                        existing_agent.districts.set(districts)
                    update_count += 1
                else:
                    # Create new agent
                    agent = Agent.objects.create(**agent_data)
                    if districts:
                        agent.districts.set(districts)
                    success_count += 1

            except Exception as e:
                error_count += 1
                errors.append(f"Error processing agent {row.get('agent_id', 'Unknown')}: {str(e)}")

        if success_count > 0:
            messages.success(self.request, f'Successfully imported {success_count} new agents.')
        if update_count > 0:
            messages.info(self.request, f'Updated {update_count} existing agents.')
        if error_count > 0:
            messages.warning(self.request, f'Failed to process {error_count} agents. See details below.')
            for error in errors:
                messages.error(self.request, error)

        return super().form_valid(form)
