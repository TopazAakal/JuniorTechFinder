from django import forms
from .models import Recruiters
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