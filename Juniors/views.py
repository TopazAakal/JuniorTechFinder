from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Juniors
from .forms import JuniorForm


def createProfile(request):
    if request.method == 'POST':
        form = JuniorForm(request.POST, request.FILES)
        if form.is_valid():
            junior = form.save()  # save the new Junior instance to the database
            # redirect to the detail page for the new Junior instance
            return redirect('showProfile', pk=junior.pk)
        else:
            print(form.errors)
            messages.error(request, "Form is not valid.")
    else:
        form = JuniorForm()
    return render(request, 'createProfile.html', {'form': form})


def showProfile(request, pk):
    # retrieve the Junior instance with the given primary key, or return a 404 error
    junior = get_object_or_404(Juniors, pk=pk)
    return render(request, 'showProfile.html', {'junior': junior})
