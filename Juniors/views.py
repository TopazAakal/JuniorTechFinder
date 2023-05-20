
import os
from django.http import HttpResponse
from django.shortcuts import render
import openai
from django.contrib.auth.decorators import login_required
from Core.decorators import group_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Juniors
from .forms import JuniorForm
from django import forms
import environ
from PyPDF2 import PdfReader

env = environ.Env()
environ.Env.read_env()


@login_required
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
    # retrieve the Junior instance with the given primary key, or return a 404 error
    junior = get_object_or_404(Juniors, pk=pk)
    default_photo_url = '/static/media/default.jpg'
    context = {'junior': junior, 'default_photo_url': default_photo_url}
    return render(request, 'showProfile.html', context)


@group_required('Junior')
def editProfile(request, pk):
    junior = get_object_or_404(Juniors, pk=pk)

    if junior.user == request.user or request.user.is_staff:
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
    else:
        return redirect("showProfile", pk=pk)


@login_required
def checkProfile(request):
    try:
        junior = request.user.juniors
        return redirect('showProfile', pk=junior.pk)
    except Juniors.DoesNotExist:
        return redirect('createProfile')


def juniorList(request):
    juniors = Juniors.objects.all()
    cities = list(set([junior.city for junior in juniors]))

    if request.method == 'GET':
        skills = request.GET.get('skills')
        city = request.GET.get('city')

        if skills:
            juniors = juniors.filter(skills__icontains=skills)

        if city:
            juniors = juniors.filter(city=city)

    return render(request, 'JuniorList.html', {'juniors': juniors, 'cities': cities})


def PDF2Text(pdfFile):
    # creating a pdf reader object
    reader = PdfReader(pdfFile)

    # printing number of pages in pdf file
    doc = len(reader.pages)
    text = []
    # getting a specific page from the pdf file
    for i in range(doc):
        page = reader.pages[i]
        text.append(page.extract_text())

    string = ""
    for i in text:
        string += i

    return string


@group_required('Junior')
def suggestions(request):
    user = request.user

    # Set the API key for the OpenAI package
    openai.api_key = env('OPENAI_API_KEY')

    # Check if the user has a Juniors profile
    try:
        junior = Juniors.objects.get(user=user)
    except Juniors.DoesNotExist:
        # Handle the case when the user doesn't have a Juniors profile
        return HttpResponse("Juniors profile not found for the user.")

    generated_text = "Upload your CV to get suggestions"

    if request.method == 'GET' and junior.cv_file:
        if not junior.generated_text:  # Check if generated_text already exists
            cv = PDF2Text(junior.cv_file)
            # Make an API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional HR recruiter that helps people to write great resumes."},
                    {"role": "user", "content": f"Task: write 4 or more suggestions on how to improve the following resume:\n {cv}"}
                ],
                n=1
            )
           # Extract the generated text from the API response
            generated_text = "\n".join(
                choice.message.content.strip() for choice in response.choices)
            junior.generated_text = generated_text  # Save generated_text to the database
            junior.save()
        else:
            generated_text = junior.generated_text  # Use the existing generated_text

    if request.method == 'POST':
        junior.cv_file = request.FILES['cv_file']
        junior.generated_text = None  # Reset generated_text when CV is updated
        junior.save()
        cv = PDF2Text(junior.cv_file)

        # Make an API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional HR recruiter that helps people to write great resumes."},
                {"role": "user", "content": f"Task: write 4 or more suggestions on how to improve the following resume:\n {cv}"}
            ],
            n=1
        )
        # Extract the generated text from the API response
        generated_text = "\n".join(choice.message.content.strip()
                                   for choice in response.choices)
        junior.generated_text = generated_text  # Save generated_text to the database
        junior.save()
    return render(request, 'suggestions.html', {'junior': junior, 'generated_text': generated_text})


@group_required('Junior')
def generate_new_suggestions(request):

    user = request.user

    # Set the API key for the OpenAI package
    openai.api_key = env('OPENAI_API_KEY')

    # Check if the user has a Juniors profile
    try:
        junior = Juniors.objects.get(user=user)
    except Juniors.DoesNotExist:
        # Handle the case when the user doesn't have a Juniors profile
        return HttpResponse("Juniors profile not found for the user.")

    junior.generated_text = None  # Reset generated_text
    junior.save()

    return redirect('suggestions')
