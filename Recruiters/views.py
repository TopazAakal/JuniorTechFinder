from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from Core.decorators import group_required
from django.contrib import messages
from .models import Recruiters, JobListing
from .forms import RecruitersForm
from django import forms
from .forms import JobListingForm
from Juniors.models import Interest
from Juniors.forms import InterestForm


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
    companies = list(set([job.company_name for job in all_jobs]))
    selected_location = request.GET.get('location')
    selected_title = request.GET.get('title')
    selected_job_type = request.GET.get('job_type')
    min_salary = request.GET.get('min_salary')
    selected_requirements = request.GET.get('requirements')
    selected_company = request.GET.get('company')

    if selected_location:
        all_jobs = all_jobs.filter(location=selected_location)
    if selected_title:
        all_jobs = all_jobs.filter(title__icontains=selected_title)
    if selected_job_type:
        all_jobs = all_jobs.filter(job_type=selected_job_type)
    if min_salary:
        all_jobs = all_jobs.filter(salary__gte=min_salary)
    if selected_requirements:
        all_jobs = all_jobs.filter(
            requirements__icontains=selected_requirements)
    if selected_company:
        all_jobs = all_jobs.filter(company_name__icontains=selected_company)

    return render(request, 'jobList.html', {'all_jobs': all_jobs, 'locations': locations, 'job_types': job_types, 'companies': companies})


@ login_required
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


def jobDetail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    form = InterestForm()
    context = {'job': job, 'form': form}
    return render(request, 'jobDetail.html', context)


@ group_required('Recruiter')
def view_applicants(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    applicants = Interest.objects.filter(job_id=job.id)
    status_choices = ['in process', 'hired', 'rejected',
                      'qualified', 'awaiting decision', 'new applicant']

    if request.method == 'POST':
        applicant_id = request.POST.get('applicant_id')
        status = request.POST.get('status')
        applicant = get_object_or_404(Interest, id=applicant_id)
        applicant.status = status
        applicant.save()
        return redirect('view_applicants', job_id=job_id)

    context = {'job': job, 'applicants': applicants,
               'status_choices': status_choices}
    return render(request, 'view_applicants.html', context)


@group_required('Recruiter')
def update_status(request):
    if request.method == 'POST':
        applicant_id = request.POST.get('applicant_id')
        new_status = request.POST.get('status')
        interest = Interest.objects.get(id=applicant_id)
        interest.status = new_status
        interest.save()
        return redirect('view_applicants', job_id=interest.job.id)
    else:
        return redirect('home')
