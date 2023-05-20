from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from Core.decorators import group_required
from django.contrib import messages
from .models import Recruiters, JobListing , Interest
from .forms import RecruitersForm
from django import forms
from .forms import JobListingForm 


@login_required
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
    recruiter = get_object_or_404(Recruiters, pk=pk)
    default_photo_url = '/static/media/default.jpg'
    saved = False
    if request.method == 'POST':
        form = RecruitersForm(request.POST, request.FILES, instance=recruiter)
        if form.is_valid():
            form.save()
            saved = True
    else:
        form = RecruitersForm(instance=recruiter)
    # Retrieve all jobs posted by the recruiter
    all_jobs = recruiter.joblisting_set.all()
    context = {'recruiter': recruiter,
               'default_photo_url': default_photo_url, 'form': form, 'saved': saved, 'all_jobs': all_jobs}
    return render(request, 'showProfileRecruiter.html', context)


@login_required
def editProfileRecruiter(request, pk):
    recruiter = get_object_or_404(Recruiters, pk=pk)

    if recruiter.user == request.user or request.user.is_staff:
        if request.method == 'POST':
            form = RecruitersForm(
                request.POST, request.FILES, instance=recruiter)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('showProfileRecruiter', pk=pk)
        else:
            form = RecruitersForm(instance=recruiter)
            form.fields['user'].widget = forms.HiddenInput()
            form.fields['user'].initial = request.user.id
        return render(request, 'editProfileRecruiter.html', {'form': form})
    else:
        return redirect("showProfileRecruiter", pk=pk)


def checkProf(request):
    try:
        recruiter = request.user.recruiters
        return redirect('showProfileRecruiter', pk=recruiter.pk)
    except Recruiters.DoesNotExist:
        return redirect('createProfileRecruiters')


@group_required('Recruiter')
def postJob(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job_listing = form.save(commit=False)
            job_listing.recruiter = request.user.recruiters if hasattr(
                request.user, 'recruiters') else request.user
            job_listing.save()
            return redirect('home')
    else:
        form = JobListingForm()

    return render(request, 'postJob.html', {'form': form})


@group_required('Recruiter')
def deleteJob(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if job.recruiter.user == request.user:
        job.delete()
        return redirect('showProfileRecruiter', pk=request.user.recruiters.pk)
    else:
        return redirect('jobDetail', job_id=job_id)


def jobList(request):
    all_jobs = JobListing.objects.all()
    locations = list(set([job.location for job in all_jobs]))
    job_types = list(set([job.job_type for job in all_jobs]))
    selected_location = request.GET.get('location')
    selected_title = request.GET.get('title')
    selected_job_type = request.GET.get('job_type')

    if selected_location:
        all_jobs = all_jobs.filter(location=selected_location)
    if selected_title:
        all_jobs = all_jobs.filter(title__icontains=selected_title)
    if selected_job_type:
        all_jobs = all_jobs.filter(job_type=selected_job_type)
    return render(request, 'jobList.html', {'all_jobs': all_jobs, 'locations': locations, 'job_types': job_types})


def jobDetail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    context = {'job': job}
    return render(request, 'jobDetail.html', context)


@login_required
def editJob(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)

    if job.recruiter.user == request.user or request.user.is_staff:
        if request.method == 'POST':
            form = JobListingForm(
                request.POST, instance=job)
            if form.is_valid():
                form.save()
                messages.success(request, 'Job updated successfully!')
                return redirect('showProfileRecruiter', pk=request.user.recruiters.pk)
        else:
            form = JobListingForm(instance=job)
            # form.fields['user'].widget = forms.HiddenInput()
           # form.fields['user'].initial = request.user.id
        return render(request, 'editJob.html', {'form': form})
    else:
        return redirect("showProfileRecruiter", pk=request.user.recruiters.pk)


def apply_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    # Additional logic for handling the application form submission and details
    context = {'job': job}
    return render(request, 'applyJob.html', context)

def submit_interest(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        resume = request.FILES.get('resume')

        # Save the form data or perform any other necessary actions
        # For example, you can save the form data to a model
        # Create a new object and save it
        interest = Interest(name=name, email=email, phone=phone, resume=resume)
        interest.save()

        # Redirect to the success page
        return redirect('home')

    # If the request method is not POST, redirect to the error page
    return redirect('home')

