from django.shortcuts import render,redirect
from Recruiters.models import Interest
from django.contrib.admin.views.decorators import user_passes_test
# Create your views here.


def reportsPage(request):
    if request.user.is_superuser:
        all_Status = Interest.objects.all()
        selected_reportsType = request.GET.get('reportType')
        if selected_reportsType=='Hired':
            all_Status = all_Status.filter(status='hired')
        return render(request, 'reports.html', {'all_Status': all_Status})
    else:
        return redirect('home')
