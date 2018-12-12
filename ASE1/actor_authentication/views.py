from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
from vendor.models import VendorProfile, VendorQty
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from customer.forms import Contact_Form
from customer.models import CustomerProfile


def customer_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        ContactForm = Contact_Form(request.POST)
        if form.is_valid() and ContactForm.is_valid():
            PhNo = ContactForm.cleaned_data.get('phone_number')
            addr = ContactForm.cleaned_data.get('address')
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            Customer_Prof = CustomerProfile.objects.get_or_create(Customer=user)[0]
            Customer_Prof.phone_number = PhNo
            Customer_Prof.address = addr
            Customer_Prof.save()
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
        ContactForm = Contact_Form()
    context = {
        'form': form,
        'ContactForm': ContactForm,
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
        return redirect('customer:actor_authentication:login_all')
    else:
        return HttpResponse('customer:home')


def vendor_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        ContactForm = Contact_Form(request.POST)
        if form.is_valid() and ContactForm.is_valid():
            PhNo = ContactForm.cleaned_data.get('phone_number')
            addr = ContactForm.cleaned_data.get('address')
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            VendorProfile.objects.create(Vendor=user)
            Customer_Prof = CustomerProfile.objects.get_or_create(Customer=user)[0]
            Customer_Prof.phone_number = PhNo
            Customer_Prof.address = addr
            Customer_Prof.save()
            return redirect('vendor:actor_authentication:login_all')
    else:
        form = UserCreationForm()
        ContactForm = Contact_Form()
    context = {
        'form': form,
        'ContactForm': ContactForm
    }
    return render(request, 'customer/signup.html', context)


def login_all(request):
    next = ""
    if request.GET:
        next = request.GET['next']

    print(next)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next == "":
                return redirect('customer:home')
            else:
                if 'nextto'and'vendorid' in request.GET:
                    nextto = request.GET['nextto']
                    vendorid = request.GET['vendorid']
                    return redirect(next + '?nextto=' + nextto +'&vendorid='+vendorid)
                else:
                    return redirect(next)


    else:
        form = AuthenticationForm
    return render(request, 'customer/login.html', {'form': form})


@login_required
def logout_all(request):
    logout(request)
    return render(request, 'customer/logout.html')


def signup_all(request):
    return render(request, 'actor_authentication/signup_all.html')
