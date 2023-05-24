from django.shortcuts import render

# Create your views here.

def reportsPage(request):
    return render(request, 'reports.html')
