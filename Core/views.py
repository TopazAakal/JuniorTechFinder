from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def homePage(request):
    return render(request, 'home.html')


def aboutUsPage(request):
    return render(request, 'aboutUs.html')


def siteRulesPage(request):
    return render(request, 'siteRules.html')


def contactUsPage(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        # print(f'Name: {name}\nEmail: {email}\nMessage: {message}')
        messages.success(request, 'Your message has been sent successfully!')
        return render(request, 'contactUs.html')
    return render(request, 'contactUs.html')
