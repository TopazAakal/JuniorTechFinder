from django.shortcuts import render
from Recruiters.models import Interest
# Create your views here.

def reportsPage(request):
    all_Status = Interest.objects.all()
    selected_reportsType = request.GET.get('reportType')
    if selected_reportsType=='Hired':
        all_Status = all_Status.filter(status='hired')
    return render(request, 'reports.html', {'all_Status': all_Status})
