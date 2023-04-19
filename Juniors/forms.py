from django import forms
from .models import Juniors


class JuniorForm(forms.ModelForm):

    class Meta:
        model = Juniors
        fields = ['full_name', 'email', 'phone_number', 'city',
                  'age', 'skills', 'summary', 'cv_file', 'photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
            'cv_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cv_file'].required = False
        self.fields['photo'].required = False
