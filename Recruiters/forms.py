from django import forms
from .models import Recruiters, JobListing,Interest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RecruitersForm(forms.ModelForm):
    user = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Recruiters
        fields = ['full_name', 'email', 'phone_number', 'city',
                  'age', 'company', 'summary', 'photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'company': forms.Textarea(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **arg):
        user = arg.pop('user', None)
        super().__init__(*args, **arg)
        if user:
            self.fields['user'].initial = user.id


class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'company_name', 'job_type','location', 'description',
                  'requirements', 'application_link', 'salary']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
        }

class InterestForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('in_process', 'In Process'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('qualified', 'Qualified'),
        ('awaiting_decision', 'Awaiting Decision'),
        ('new_applicant', 'New Applicant')
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='new_applicant')  # Set the default value

    class Meta:
        model = Interest
        fields = ['name', 'email', 'phone', 'resume', 'status']
        widgets = {
            'resume': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }
