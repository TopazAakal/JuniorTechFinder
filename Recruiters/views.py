from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Recruiters, JobListing
from .forms import RecruitersForm
from django import forms
from .forms import JobListingForm


def createProfileRecruiters(request):
    user = request.user
    if hasattr(user, 'recruiters'):
        return redirect('checkProf')

    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['user'] = request.user.id
        form = RecruitersForm(form_data, request.FILES)
        if form.is_valid():
            recruiter = form.save(commit=False)
            recruiter.user = user
            recruiter.save()
            return redirect('checkProf')
    else:
        form = RecruitersForm()
        form.fields['user'].widget = forms.HiddenInput()
        form.fields['user'].initial = user.id

    return render(request, 'createProfileRecruiters.html', {'form': form})


def showProfileRecruiter(request, pk):
    recruiter = get_object_or_404(Recruiters, pk=pk, user=request.user)
    default_photo_url = '/static/media/default.jpg'
    saved = False
    if request.method == 'POST':
        form = RecruitersForm(request.POST, request.FILES, instance=recruiter)
        if form.is_valid():
            form.save()
            saved = True
    else:
        form = RecruitersForm(instance=recruiter)

    context = {'recruiter': recruiter,
               'default_photo_url': default_photo_url, 'form': form, 'saved': saved}
    return render(request, 'showProfileRecruiter.html', context)


def checkProf(request):
    try:
        recruiter = request.user.recruiters
        return redirect('showProfileRecruiter', pk=recruiter.pk)
    except Recruiters.DoesNotExist:
        return redirect('createProfileRecruiters')


def postJob(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job_listing = form.save(commit=False)
            job_listing.recruiter = request.user
            job_listing.save()
            return redirect('home')
    else:
        form = JobListingForm()

    return render(request, 'postJob.html', {'form': form})
