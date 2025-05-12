from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib import messages
from .models import Agent, Incentive
from .forms import AgentForm, AgentBulkUploadForm, MemberAgentRelationshipForm, IncentiveForm
from cooperatives.mixins import CustomLoginRequiredMixin
from django.db.models import Q, F
import csv
import io
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from cooperatives.models import Member

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
        
        # Get all agents for statistics
        agents = Agent.objects.all()
        
        # Total agents count
        context['total_agents'] = agents.count()
        
        # Active agents count
        context['active_agents'] = agents.filter(is_active=True).count()
        
        # Agents with incomplete profiles
        incomplete_profiles = agents.filter(
            Q(phone_number='') | 
            Q(phone_number__isnull=True) |
            Q(last_name='') |
            Q(last_name__isnull=True) |
            Q(email='') |
            Q(email__isnull=True)
        ).count()
        context['incomplete_profiles'] = incomplete_profiles
        
        # Best performing agent (based on farmers profiled)
        best_agent = agents.filter(is_active=True).order_by('-farmers_profiled').first()
        context['best_agent'] = best_agent
        
        # Recently joined agents (last 30 days)
        from datetime import timedelta
        from django.utils import timezone
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        context['new_agents'] = agents.filter(date_joined__gte=thirty_days_ago).count()
        
        # Agents by gender
        context['male_agents'] = agents.filter(gender='M').count()
        context['female_agents'] = agents.filter(gender='F').count()
        
        return context

class AgentDetailView(LoginRequiredMixin, DetailView):
    model = Agent
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent = self.get_object()
        
        # Ensure agent has a user account
        if not agent.user:
            agent.create_user_account()
        
        # Get profiled farmers with pagination
        profiled_farmers = Member.objects.filter(created_by=agent.user)
        paginator = Paginator(profiled_farmers, 50)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get current active incentive
        current_incentive = Incentive.objects.filter(is_active=True).first()
        
        # Calculate total incentive amount
        total_incentive = 0
        if current_incentive:
            total_incentive = current_incentive.price_per_farmer * agent.farmers_profiled
        
        # Get incentive history
        incentive_history = Incentive.objects.all().order_by('-created_at')
        
        context.update({
            'page_obj': page_obj,
            'current_incentive': current_incentive,
            'incentive_history': incentive_history,
            'incentive_form': IncentiveForm(),
            'total_incentive': total_incentive,
        })
        return context

    def post(self, request, *args, **kwargs):
        form = IncentiveForm(request.POST)
        
        if form.is_valid():
            incentive = form.save(commit=False)
            incentive.save()
            messages.success(request, 'Global incentive rate updated successfully.')
        else:
            messages.error(request, 'Error updating incentive rate. Please check the form.')
        
        return redirect('agents:agent-detail', pk=self.get_object().pk)

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

    def parse_date(self, date_str):
        """Try multiple date formats and return parsed date"""
        if not date_str:
            return None
            
        date_formats = [
            '%Y-%m-%d',  # YYYY-MM-DD
            '%d-%m-%Y',  # DD-MM-YYYY
            '%d/%m/%Y',  # DD/MM/YYYY
            '%Y/%m/%d',  # YYYY/MM/DD
        ]
        
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str.strip(), date_format).date()
            except ValueError:
                continue
        return None

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
        
        # Validate required columns - only agent_id, first_name, and gender are required
        required_columns = ['agent_id', 'first_name', 'gender']
        optional_columns = ['last_name', 'email', 'phone_number', 'date_of_birth', 'date_joined', 'districts', 'farmers_profiled']
        
        missing_columns = [col for col in required_columns if col not in reader.fieldnames]
        if missing_columns:
            messages.error(self.request, f'Missing required columns: {", ".join(missing_columns)}')
            return self.form_invalid(form)
        
        success_count = 0
        error_count = 0
        update_count = 0
        errors = []
        row_number = 1  # Start counting from 1 to match spreadsheet row numbers

        for row in reader:
            row_number += 1
            row_errors = []
            
            try:
                # Clean whitespace from all fields
                row = {k: v.strip() if v else v for k, v in row.items()}
                
                # Validate required fields
                for field in required_columns:
                    if not row.get(field):
                        row_errors.append(f"Missing required field: {field}")
                
                # Validate email format if provided
                if row.get('email'):
                    if '@' not in row['email']:
                        row_errors.append("Invalid email format")
                
                # Validate phone number format if provided
                if row.get('phone_number'):
                    if not row['phone_number'].isdigit():
                        row_errors.append("Phone number must contain only digits")
                
                # Validate gender
                if row.get('gender') and row['gender'].upper() not in ['M', 'F']:
                    row_errors.append("Gender must be 'M' or 'F'")
                
                # Parse dates with flexible format
                date_of_birth = self.parse_date(row.get('date_of_birth'))
                if row.get('date_of_birth') and not date_of_birth:
                    row_errors.append("Invalid date_of_birth format (use DD-MM-YYYY or YYYY-MM-DD)")
                
                date_joined = self.parse_date(row.get('date_joined'))
                if row.get('date_joined') and not date_joined:
                    row_errors.append("Invalid date_joined format (use DD-MM-YYYY or YYYY-MM-DD)")
                
                # Validate farmers_profiled if provided
                if row.get('farmers_profiled'):
                    try:
                        int(row['farmers_profiled'])
                    except ValueError:
                        row_errors.append("farmers_profiled must be a number")
                
                # If there are any validation errors, add them to the errors list and skip this row
                if row_errors:
                    errors.append(f"Row {row_number} ({row.get('agent_id', 'Unknown')}): {', '.join(row_errors)}")
                    error_count += 1
                    continue
                
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
                        row_errors.append(f"District '{name}' not found")

                # Create agent with required fields
                agent_data = {
                    'agent_id': row['agent_id'],
                    'first_name': row['first_name'],
                    'gender': row['gender'].upper(),
                    'is_active': True,
                }

                # Add optional fields if they exist
                if row.get('last_name'):
                    agent_data['last_name'] = row['last_name']
                else:
                    agent_data['last_name'] = ''  # Empty string for last_name if not provided
                    
                if row.get('email'):
                    agent_data['email'] = row['email']
                    
                if row.get('phone_number'):
                    agent_data['phone_number'] = row['phone_number']
                else:
                    agent_data['phone_number'] = ''  # Empty string for phone_number if not provided

                # Add dates if they were successfully parsed
                if date_of_birth:
                    agent_data['date_of_birth'] = date_of_birth
                else:
                    agent_data['date_of_birth'] = datetime(1990, 1, 1).date()  # Default date if not provided

                if date_joined:
                    agent_data['date_joined'] = date_joined

                if row.get('farmers_profiled'):
                        agent_data['farmers_profiled'] = int(row['farmers_profiled'])

                # Check if agent already exists by agent_id instead of email
                existing_agent = Agent.objects.filter(agent_id=row['agent_id']).first()
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
                errors.append(f"Row {row_number} ({row.get('agent_id', 'Unknown')}): {str(e)}")

        # Display summary messages
        if success_count > 0:
            messages.success(self.request, f'Successfully imported {success_count} new agents.')
        if update_count > 0:
            messages.info(self.request, f'Updated {update_count} existing agents.')
        if error_count > 0:
            messages.warning(self.request, f'Failed to process {error_count} agents. See details below.')
            # Display errors in groups of 5 to avoid overwhelming the user
            for i in range(0, len(errors), 5):
                error_group = errors[i:i+5]
                messages.error(self.request, '<br>'.join(error_group))

        return super().form_valid(form)

class MemberAgentRelationshipView(LoginRequiredMixin, FormView):
    template_name = 'agents/member_agent_relationship.html'
    form_class = MemberAgentRelationshipForm
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
        
        # Validate required columns
        required_columns = ['member_id', 'agent_id']
        missing_columns = [col for col in required_columns if col not in reader.fieldnames]
        if missing_columns:
            messages.error(self.request, f'Missing required columns: {", ".join(missing_columns)}')
            return self.form_invalid(form)
        
        # Initialize counters and logs
        success_count = 0
        error_count = 0
        admin_count = 0
        missing_agent_count = 0
        missing_member_count = 0
        reassigned_count = 0
        skipped_count = 0
        missing_agents = set()
        missing_members = set()
        invalid_agent_ids = set()
        reassigned_members = set()
        skipped_members = set()
        row_errors = {}  # Dictionary to store errors by row number
        row_number = 1  # Start counting from 1 to match spreadsheet row numbers

        # Pre-fetch all members and their created_by information
        members = Member.objects.all().select_related('created_by')
        member_dict = {member.member_id: member for member in members}

        # Get admin user
        from django.contrib.auth.models import User
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            messages.error(self.request, 'Admin user not found. Please create a superuser first.')
            return self.form_invalid(form)

        # Pre-fetch all agents for faster lookup
        all_agents = list(Agent.objects.all())
        agent_dict = {agent.id: agent for agent in all_agents}

        # Track which members are assigned to which agents
        agent_members = {}  # agent_id -> set of member_ids

        for row in reader:
            row_number += 1
            current_row_errors = []
            
            try:
                # Clean whitespace from all fields
                row = {k: v.strip() if v else v for k, v in row.items()}
                
                # Validate required fields
                if not row.get('member_id'):
                    current_row_errors.append(f"Missing required field: member_id")
                    error_count += 1
                    row_errors[row_number] = current_row_errors
                    continue
                
                # Check if member exists
                member = member_dict.get(row['member_id'])
                if not member:
                    missing_member_count += 1
                    missing_members.add(row['member_id'])
                    current_row_errors.append(f"Member ID {row['member_id']} not found in system")
                    error_count += 1
                    row_errors[row_number] = current_row_errors
                    continue

                # Handle admin case
                if row.get('agent_id', '').lower() == 'admin':
                    if member.created_by:
                        # Decrease old agent's count if it exists
                        old_agent = Agent.objects.filter(
                            first_name__iexact=member.created_by.first_name,
                            last_name__iexact=member.created_by.last_name
                        ).first()
                        if old_agent:
                            old_agent.farmers_profiled = F('farmers_profiled') - 1
                            old_agent.save()
                        reassigned_count += 1
                        reassigned_members.add(row['member_id'])
                    member.created_by = admin_user
                    member.save()
                    admin_count += 1
                    success_count += 1
                    continue
                
                # Get agent ID
                try:
                    agent_id = int(row['agent_id'])
                except (ValueError, TypeError):
                    invalid_agent_ids.add(row['agent_id'])
                    current_row_errors.append(f"Invalid agent ID: {row['agent_id']}")
                    error_count += 1
                    row_errors[row_number] = current_row_errors
                    continue
                
                # Check if agent exists
                agent = agent_dict.get(agent_id)
                if not agent:
                    missing_agent_count += 1
                    missing_agents.add(str(agent_id))
                    current_row_errors.append(f"Agent ID {agent_id} not found in system")
                    error_count += 1
                    row_errors[row_number] = current_row_errors
                    continue
                
                # Initialize the set for this agent if not exists
                if agent.id not in agent_members:
                    agent_members[agent.id] = set()
                
                # Check if member is already assigned to this agent
                if member.member_id in agent_members[agent.id]:
                    skipped_count += 1
                    skipped_members.add(row['member_id'])
                    continue
                
                # Find or create user for the agent
                agent_user = User.objects.filter(
                    first_name__iexact=agent.first_name,
                    last_name__iexact=agent.last_name
                ).first()
                
                if not agent_user:
                    # Create a new user for the agent
                    agent_user = User.objects.create(
                        username=f"{agent.first_name.lower()}_{agent.last_name.lower()}",
                        first_name=agent.first_name,
                        last_name=agent.last_name,
                        email=f"{agent.first_name.lower()}.{agent.last_name.lower()}@example.com",
                        is_staff=True
                    )
                
                # If member already has an agent, decrease old agent's count
                if member.created_by:
                    old_agent = Agent.objects.filter(
                        first_name__iexact=member.created_by.first_name,
                        last_name__iexact=member.created_by.last_name
                    ).first()
                    if old_agent:
                        old_agent.farmers_profiled = F('farmers_profiled') - 1
                        old_agent.save()
                    reassigned_count += 1
                    reassigned_members.add(row['member_id'])
                
                # Update member's created_by field
                member.created_by = agent_user
                member.save()
                
                # Add member to agent's set
                agent_members[agent.id].add(member.member_id)
                
                # Update new agent's farmers_profiled count
                agent.farmers_profiled = F('farmers_profiled') + 1
                agent.save()
                success_count += 1

            except Exception as e:
                error_count += 1
                row_errors[row_number] = [f"Unexpected error: {str(e)}"]

        # Display summary messages
        if success_count > 0:
            messages.success(self.request, f'Successfully processed {success_count} records.')
        
        if admin_count > 0:
            messages.info(self.request, f'Assigned {admin_count} members to admin.')
        
        if reassigned_count > 0:
            messages.info(self.request, f'Reassigned {reassigned_count} members to new agents.')
        
        if skipped_count > 0:
            messages.info(self.request, f'Skipped {skipped_count} members already assigned to their agents.')
        
        if missing_agent_count > 0:
            messages.warning(self.request, f'Found {missing_agent_count} records with agents not in system. Missing agent IDs: {", ".join(sorted(missing_agents))}')
        
        if missing_member_count > 0:
            messages.warning(self.request, f'Found {missing_member_count} records with members not in system. Missing member IDs: {", ".join(sorted(missing_members))}')
        
        if invalid_agent_ids:
            messages.warning(self.request, f'Found {len(invalid_agent_ids)} records with invalid agent IDs. Invalid IDs: {", ".join(sorted(invalid_agent_ids))}')
        
        if error_count > 0:
            messages.warning(self.request, f'Encountered {error_count} errors during processing.')
            # Display detailed error messages in groups of 5
            error_messages = []
            for row_num, errors in row_errors.items():
                error_messages.append(f"Row {row_num}: {', '.join(errors)}")
            
            # Display errors in groups of 5
            for i in range(0, len(error_messages), 5):
                error_group = error_messages[i:i+5]
                messages.error(self.request, '<br>'.join(error_group))

        return super().form_valid(form)

class GlobalIncentiveView(LoginRequiredMixin, ListView):
    model = Incentive
    template_name = 'agents/global_incentive.html'
    context_object_name = 'incentives'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_incentive'] = Incentive.objects.filter(is_active=True).first()
        context['incentive_form'] = IncentiveForm()
        return context

    def post(self, request, *args, **kwargs):
        form = IncentiveForm(request.POST)
        
        if form.is_valid():
            incentive = form.save(commit=False)
            incentive.save()
            messages.success(request, 'Global incentive rate updated successfully.')
        else:
            messages.error(request, 'Error updating incentive rate. Please check the form.')
        
        return redirect('agents:global-incentive')
