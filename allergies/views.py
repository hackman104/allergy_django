from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import Link, Request
from .forms import RequestForm

# Create your views here.
def index(request):
    """Loads the home page for allergies app"""
    return render(request, 'allergies/index.html')

def search(request):
    """Loads the search page for the allergies app"""
    rest_list = Link.objects.order_by('restaurant_name')
    context = {'rest_list': rest_list}
    return render(request, 'allergies/search.html', context)

def ask(request):
    """Loads the request page for the allergies app if GET, writes request to
       database if successful POST"""
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.request_date = timezone.now()
            req.save()
        return HttpResponseRedirect(reverse('allergies:request'))

    elif request.method == 'GET':
        form = RequestForm()
        return render(request, 'allergies/request.html', {'form': form})


def contact(request):
    """Loads the contact page for the allergies app"""
    return HttpResponse("This is a placeholder for the contact page")