from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Juniors

from .forms import JuniorForm
from django import forms


def createProfile(request):
    user = request.user
    if hasattr(user, 'juniors'):
        return redirect('checkProfile')

    if request.method == 'POST':
        form_data = request.POST.copy()  # Make a copy of the POST data
        form_data['user'] = request.user.id  # Add the user id to the form data
        form = JuniorForm(form_data, request.FILES)
        # form = JuniorForm(request.POST, request.FILES)
        if form.is_valid():
            junior = form.save(commit=False)
            junior.user = user
            junior.save()
            return redirect('checkProfile')
    else:
        form = JuniorForm()
        form.fields['user'].widget = forms.HiddenInput()
        form.fields['user'].initial = user.id

    return render(request, 'createProfile.html', {'form': form})


def showProfile(request, pk):
    # retrieve the Junior instance with the given primary key and the current user's ID, or return a 404 error
    junior = get_object_or_404(Juniors, pk=pk, user=request.user)
    default_photo_url = '/static/media/default.jpg'
    context = {'junior': junior, 'default_photo_url': default_photo_url}
    return render(request, 'showProfile.html', context)


def editProfile(request, pk):

    junior = get_object_or_404(Juniors, pk=pk, user=request.user)

    if request.method == 'POST':
        form = JuniorForm(request.POST, request.FILES, instance=junior)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('showProfile', pk=pk)
    else:
        form = JuniorForm(instance=junior)
        form.fields['user'].widget = forms.HiddenInput()
        form.fields['user'].initial = request.user.id

    return render(request, 'editProfile.html', {'form': form})


def checkProfile(request):
    try:
        junior = request.user.juniors
        return redirect('showProfile', pk=junior.pk)
    except Juniors.DoesNotExist:
        return redirect('createProfile')
