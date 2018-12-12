from django.db.models import Q
from django.shortcuts import render, redirect
from cart.models import Order
from vendor.forms import ProductsAdd
from vendor.models import Product, Category, VendorQty
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from ASE1.decorators import vendor_required


def index(request):
    return render(request, 'vendor/base.html')


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


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def add_products(request):
    if request.method == 'POST':
        form = ProductsAdd(request.POST, request.FILES)
        if form.is_valid():
            a = form.save()
            profile = VendorQty.objects.get_or_create(Vendor=request.user, product=a)[0]
            profile.qty = form.cleaned_data['quantity']
            profile.save()
            return redirect('vendor:view_products')

    else:
        form = ProductsAdd()
    return render(request, 'vendor/add_products.html', {'form': form})


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def view_products(request):
    product_list = Product.objects.all().order_by('prod_name')
    current_order_products = []
    query = request.GET.get('q')
    if query:
        product_list = Product.objects.filter(
            Q(prod_name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__cat_name__contains=query)
        )
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'vendor/view_products.html', {'products': products})


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def modify_products(request, id):
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        form = ProductsAdd(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            profile = VendorQty.objects.get_or_create(Vendor=request.user, product=product)[0]
            profile.qty = form.cleaned_data['quantity']
            profile.save()
            # product.qty.add(profile)
            return redirect('vendor:view_products')
    else:
        q = VendorQty.objects.get_or_create(Vendor=request.user, product=product)[0]

        data = {
            'quantity': q.qty
        }
        form = ProductsAdd(instance=product, initial=data)
    return render(request, 'vendor/modify_product.html', {'form': form})


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def delete_product(request, id):
    product = Product.objects.get(pk=id)
    name = product.prod_name
    product.delete()
    return render(request, 'vendor/deleted.html', {'name': name})


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def view_orders(request):
    orders = Order.objects.filter(is_ordered=True, vendor=request.user)
    return render(request, 'vendor/show_orders.html', {'orders': orders})


def Search_Results(request):
    products = []
    current_order_products = []
    query = request.GET.get('q')
    # print(query)
    if query:
        products = Product.objects.filter(
            Q(prod_name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__cat_name__contains=query)
        )
    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.cus)
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]
    context = {
        "products": products,
        "current_order_products": current_order_products,
    }
    return render(request, 'customer/search_results.html', context)
