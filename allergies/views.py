from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from itertools import chain
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

from .models import Link, Request
from .forms import RequestForm, ContactForm

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
            messages.success(request, "Your request has been successfully processed.")
        else:
            messages.error(request, "There was a problem processing your request.")
        return HttpResponseRedirect(reverse('allergies:request'))

    elif request.method == 'GET':
        form = RequestForm()
        context = {'form': form}
        return render(request, 'allergies/request.html', context)

def lookup(request):
    """Search for restaurants similar to query"""

    if not request.GET['q']:
        raise RuntimeError("missing query")

    q = request.GET['q']

    # search database for objects similar to user query
    entries = Link.objects.filter(restaurant_name__startswith=q).values('restaurant_name', 'rest_link')
    
    # convert to json to pass to jquery
    entries_json = json.dumps(list(entries), cls=DjangoJSONEncoder)
	
    return HttpResponse(entries_json, content_type='application/json')

def check(request, st):
    """Check to ensure requested restaurant is not already available in database"""
    
    # ensure parameter was passed correctly
    try:
        name = st
    except:
        raise RuntimeError("Missing query")
    
    # check both tables for a restaurant whose name matches that requested, combine results
    link_list = Link.objects.filter(restaurant_name=name).values('restaurant_name')
    request_list = Request.objects.filter(request_name=name).values('request_name')

    #convert to json and pass back
    link_list_json = json.dumps(list(link_list), cls=DjangoJSONEncoder)
    request_list_json = json.dumps(list(request_list), cls=DjangoJSONEncoder)

    if len(link_list_json) > 2:
        return HttpResponse(link_list_json, content_type='application/json')
    else:
        return HttpResponse(request_list_json, content_type='application/json')

    
def contact(request):
    """Loads the contact page for the allergies app"""
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['allergy.list.website@gmail.com'])
            except BadHeaderError:
                return HttpResponse("Invalid email header information")
            return redirect('success')
    return render(request, "email.html", {'form': form})

def success(request):
    """Displays a success message that the user's message was sent"""
    return HttpResponse("Your message was successfully sent!")
