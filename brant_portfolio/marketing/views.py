from django.shortcuts import render, redirect
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
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, (from_email + ': ' + message), from_email, ['brantmort@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "email.html", {'form': form})

