import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.views.generic.base import TemplateView
from .forms import ContactForm

from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError

class HomePage(TemplateView):
    template_name = 'index.html'

class Success(TemplateView):
    template_name = 'success.html'

def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''


            if result['success']:
                subject = form.cleaned_data['subject']
                from_email = form.cleaned_data['from_email']
                message = form.cleaned_data['message']
                try:
                    send_mail(subject, (from_email + ': ' + message), from_email, ['brantmort@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

                return redirect('thanks')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return redirect('/#application-form')
            

    return render(request, "email.html", {'form': form})

