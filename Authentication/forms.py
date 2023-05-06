from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# LoginForm class for user login form
class LoginForm(forms.Form):
    # Form fields for username and password
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

# SignUpForm class for user signup form, extending UserCreationForm


class SignUpForm(UserCreationForm):
    # Form fields for email, first name, last name, password1 and password2
    email = forms.EmailField(
        max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Required.')
    role = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        # Set model as User and include required fields
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'role', 'password1', 'password2')
        # Set widgets for each field for class styling
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        # Custom clean method to set username as email
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        self.cleaned_data['username'] = email
        return cleaned_data
