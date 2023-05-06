from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import auth, messages

# This view is responsible for handling the user login functionality


def login_view(request):
    # If user is already authenticated, redirect them to the home page
    if request.user.is_authenticated:
        return redirect('home')
    # If request method is POST, validate form and attempt login
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # If user is authenticated, log them in and redirect to home page
                auth.login(request, user)
                return redirect('home')
            else:
                # If user authentication fails, add error to form
                form.add_error(None, 'Invalid username or password')
    else:
        # If request method is GET, show login form
        form = LoginForm()

    # Render the login page with the form object
    return render(request, 'login.html', {'form': form})


# This view is responsible for handling the user signup functionality
def signup_view(request):
    # If user is already authenticated, redirect them to the home page
    if request.user.is_authenticated:
        return redirect('home')

    # If request method is POST, validate form and attempt user creation
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('username')
            if User.objects.filter(email=email).exists():
                # If user with the same email already exists, add error to form and show signup page again
                form.add_error(
                    'email', 'A user with that email already exists.')
                return render(request, 'signup.html', {'form': form})
            user.username = email
            role = form.cleaned_data.get('role')
            user.save()
            user.groups.add(role)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            # Log the user in and redirect to home page
            login(request, user)
            return redirect('home')
            # return redirect('checkProfileUser')

    else:
        # If request method is GET, show signup form
        form = SignUpForm()

    # Render the signup page with the form object
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    # messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# def checkProfileUser(request):
#     if request.user.groups.filter(name='Junior').exists():
#         return redirect('createProfile')
#     else:
#         return redirect('createProfileRecruiters')
