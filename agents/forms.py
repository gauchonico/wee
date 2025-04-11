from django import forms
from .models import Agent
from cooperatives.models import District

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'agent_id', 'first_name', 'last_name', 'email',
            'gender', 'date_of_birth', 'phone_number',
            'is_active', 'districts', 'farmer_groups'
        ]
        widgets = {
            'agent_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'districts': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'farmer_groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number

    def clean_agent_id(self):
        agent_id = self.cleaned_data.get('agent_id')
        if Agent.objects.filter(agent_id=agent_id).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("This agent ID is already in use.")
        return agent_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Agent.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class AgentBulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with the following columns: agent_id, first_name, last_name, email, phone_number, gender, date_of_birth, districts, farmers_profiled. Districts should be comma-separated if multiple (e.g. "agago, pader").'
    ) 