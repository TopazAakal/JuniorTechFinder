from django.shortcuts import render
from django.http import HttpResponse


def homePage(request):
    return render(request, 'home.html')

def aboutUsPage(request):
    return render(request, 'aboutUs.html')


