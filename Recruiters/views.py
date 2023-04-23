from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Recruiters
from .forms import RecruitersForm


def createProfileRecruiters(request):

    if request.method == 'POST':
        form = RecruitersForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                recruiter = form.save()  # save the new Junior instance to the database
                # redirect to the detail page for the new Junior instance
                return redirect('showProfileRecruiter.html', pk=recruiter.pk)
            except Exception as e:
                messages.error(request, f"Error saving form: {e}")
        else:
            form.add_error(
                'email', "Form is not valid.")
            # print(form.errors)
            # messages.error(request, "Form is not valid.")
    else:
        form = RecruitersForm()
    return render(request, 'createProfileRecruiters.html', {'form': form})


def showProfileRecruiter(request, pk):
    recruiter = get_object_or_404(Recruiters, pk=pk)

    if request.method == 'POST':
        recruiter.full_name = request.POST.get('full_name')
        recruiter.email = request.POST.get('email')
        recruiter.phone_number = request.POST.get('phone_number')
        recruiter.city = request.POST.get('city')
        recruiter.age = request.POST.get('age')
        recruiter.summary = request.POST.get('summary')
        recruiter.company = request.POST.get('company')
        if request.FILES.get('photo'):
            recruiter.photo = request.FILES.get('photo')
        recruiter.save()

    return render(request, 'showProfileRecruiter.html', {'recruiter': recruiter})
