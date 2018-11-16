from datetime import datetime
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .forms import UserCreationForm
from customer.models import CustomerProfile
from vendor.models import VendorProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


# Create your views here.
###########   EARLIER   ########################
# def customer_signup(request):
#     if request.method == 'POST':
#         form = CustomerCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             contact_number = form.cleaned_data['contact_number']
#             c = CustomerProfile.objects.get(Customer=user)
#             # send_mail('Hello Customer', 'Thanks for registering', settings.EMAIL_HOST_USER, [user.email],
#             #           fail_silently=True)
#             c.phone_number = contact_number
#             login(request, user)
#             return redirect('customer:home')
#     else:
#         form = CustomerCreationForm()
#     return render(request, 'customer/signup.html', {'form': form})
###########   EARLIER   ########################

def customer_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('actor_authentication/actimail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'customer/signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('customer:home')


###########   EARLIER   ########################
# def vendor_signup(request):
#     if request.method == 'POST':
#         form = VendorCreationForm(request.POST)
#
#         if form.is_valid():
#             user = form.save()
#             contact_number = form.cleaned_data['contact_number']
#             # new_vendor = VendorProfile(Vendor=user,phone_number=contact_number)
#             VendorProfile.objects.create(Vendor=user, phone_number=contact_number)
#             # send_mail('Hello vendor', 'Thanks for registering', settings.EMAIL_HOST_USER, [user.email],
#             #           fail_silently=True)
#             login(request, user)
#             return redirect('vendor:view_products')
#     else:
#         form = VendorCreationForm()
#     return render(request, 'vendor/signup.html', {'form': form})
###########   EARLIER   ########################

def vendor_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            VendorProfile.objects.create(Vendor=user)
            return redirect('vendor:actor_authentication:login_all')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/signup.html', context)


def login_all(request):
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


@login_required
def logout_all(request):
    logout(request)
    return render(request, 'customer/logout.html')


def signup_all(request):
    return render(request, 'actor_authentication/signup_all.html')
