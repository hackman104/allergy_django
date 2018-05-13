from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
import requests
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from functools import wraps

from .models import Link, Request
from .forms import RequestForm, ContactForm

def check_recaptcha(view_func):
    """Decorator for reCAPTCHA validation"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == "POST":
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, "Invalid reCAPTCHA. Please try again.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Create your views here.
def index(request):
    """Loads the home page for allergies app"""
    return render(request, 'allergies/index.html')

def search(request):
    """Loads the search page for the allergies app"""
    rest_list = Link.objects.order_by('restaurant_name')
    context = {'rest_list': rest_list}
    return render(request, 'allergies/search.html', context)

@check_recaptcha
def ask(request):
    """Loads the request page for the allergies app if GET, writes request to
       database if successful POST"""
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            req = form.save(commit=False)
            req.request_date = timezone.now()
            req.save()
            messages.success(request, "Your request has been successfully processed.")
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

#def contact(request):
#    if request.method == 'GET':
#        form = ContactForm()
#    else:
#        form = ContactForm(request.POST)
#        if form.is_valid():
#            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('EMAIL_API_PASS'))
#            from_email = Email(form.cleaned_data['from_email'])
#            to_email = Email("allergy.list.website@gmail.com")
#            subject = form.cleaned_data['subject']
#            content = Content("text/plain", form.cleaned_data['message'])
#            mail = Mail(from_email, subject, to_email, content)
#            response = sg.client.mail.send.post(request_body=mail.get())
#            print(response.status_code)
#            print(response.body)
#            print(response.headers)
#            messages.success(request, "Your email has been sent.")
#            return HttpResponseRedirect(reverse('allergies:contact'))
#    return render(request, "allergies/email.html", {'form': form})

@check_recaptcha
def contact(request):
    """Loads the contact page for the allergies app"""
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            messages.success(request, "Your email has been sent.")
            try:
                send_mail(subject, message, from_email, ['allergy.list.website@gmail.com'])
            except BadHeaderError:
                return HttpResponse("Invalid email header information")
            return HttpResponseRedirect(reverse('allergies:contact'))
        else:
            form = ContactForm()
    return render(request, "allergies/email.html", {'form': form})



#def successView(request):
#    """Displays a success message that the user's message was sent"""
#    return render(request, "allergies/success.html")
