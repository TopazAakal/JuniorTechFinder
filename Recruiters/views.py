from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Recruiters
from .forms import RecruitersForm
from django import forms

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
    context = {'recruiter': recruiter, 'default_photo_url': default_photo_url}
    return render(request, 'showProfileRecruiter.html', context)


def checkProf(request):
    try:
        recruiter = request.user.recruiters
        return redirect('showProfileRecruiter', pk=recruiter.pk)
    except Recruiters.DoesNotExist:
        return redirect('createProfileRecruiters')