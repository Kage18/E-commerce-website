from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.conf import settings
from customer.models import CustomerProfile
from customer.forms import CustomerCreationForm
from django.views import generic
from vendor.models import Category, Product
from cart.models import order

def home(request):
    return HttpResponse('Dear Customer, welcome to the home page!')


def index(request):
    return render(request, 'customer/base.html')


def profile(request):
    a = request.user
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']

        a.username = username
        a.first_name = first_name
        a.last_name = last_name
        a.email = email
        a.cus.phone_number = phone
        a.cus.save()
        a.save()
        return redirect('customer:home')

    return render(request, 'customer/profile.html')


def ItemsView(request,pk):
    cat = Category.objects.get(id=pk)
    filtered_orders = order.objects.filter(owner=request.user.cus, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]

    context = {
        'cat': cat,
        'current_order_products': current_order_products
    }

    return render(request, "customer/items.html", context)


class IndexView(generic.ListView):
    template_name = 'customer/index.html'
    context_object_name = 'cat'

    def get_queryset(self):
        return Category.objects.all()


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            contact_number = form.cleaned_data['contact_number']
            #CustomerProfile.objects.create(Customer=user, phone_number=contact_number)
            send_mail('Hello Customer', 'Thanks for registering', settings.EMAIL_HOST_USER, [user.email],
                      fail_silently=True)
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
