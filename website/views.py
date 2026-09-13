from django.shortcuts import render
from django.http import *
from website.models import Contact
from website.forms import ContactForm, NewsletterForm
from django.contrib import messages

def index_view(request):
    return render(request, 'website/index.html')

def about_view(request):
    return render(request, 'website/about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.name = 'anonymous'
            if not contact.subject:
                contact.subject = None
            contact.save()
            messages.add_message(request, messages.SUCCESS, 'Your ticket submited successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Your ticket did not submited')

    form = ContactForm()
    return render(request, 'website/contact.html', {'form': form})


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'You subscribed successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Your email is not valid')
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

           
def test_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            print(name, email, subject, message)
            return HttpResponse('done')
        else:
            return HttpResponse('not valid')

    form = ContactForm()
    return render(request, 'test.html', {'form':form})