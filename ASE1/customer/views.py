from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.conf import settings
from customer.models import CustomerProfile
from customer.forms import CustomerCreationForm


def home(request):
    return HttpResponse('Dear Customer, welcome to the home page!')


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            contact_number = form.cleaned_data['contact_number']
            CustomerProfile.objects.create(Customer=user, phone_number=contact_number)

            send_mail('Hello Customer', 'Thanks for registering', settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
            login(request, user)
            return redirect('customer:home')
    else:
        form = CustomerCreationForm()
    return render(request, 'customer/signup.html', {'form': form})


def customer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('customer:home')
    else:
        form = AuthenticationForm
    return render(request, 'customer/login.html', {'form': form})


def customer_logout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'customer/logout.html')
    else:
        return HttpResponse('Cannot hard code logout')
