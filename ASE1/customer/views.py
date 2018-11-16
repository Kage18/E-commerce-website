from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from customer.forms import CustomerCreationForm
from django.views import generic
from vendor.models import Category
from cart.models import Order
from customer.models import CustomerProfile
from django.contrib.auth.decorators import login_required


def get_user_order(request):
    user_profile = get_object_or_404(CustomerProfile, Customer=request.user)
    ord = Order.objects.filter(owner=user_profile, is_ordered=True)
    if ord.exists():
        return ord
    return 0


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

    placed_order = get_user_order(request)
    context = {
        'ordre': placed_order
    }
    return render(request, 'customer/profile.html', context)


def itemsview(request, pk):
    cat = Category.objects.get(id=pk)
    current_order_products = []
    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.cus, is_ordered=False)
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]

    context = {
        'cat': cat,
        'current_order_products': current_order_products
    }

    return render(request, "customer/items.html", context)


def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'customer/index.html', {'categories': categories})


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            contact_number = form.cleaned_data['contact_number']
            c = CustomerProfile.objects.get(Customer=user)
            # send_mail('Hello Customer', 'Thanks for registering', settings.EMAIL_HOST_USER, [user.email],
            #           fail_silently=True)
            c.phone_number = contact_number
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


@login_required
def customer_logout(request):
    logout(request)
    return render(request, 'customer/logout.html')
