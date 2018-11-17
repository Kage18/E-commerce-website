from django.shortcuts import render, redirect
from django.http import HttpResponse

from cart.models import Order
from vendor.forms import ProductsAdd
from vendor.models import Product, Category
from django.contrib.auth.decorators import login_required
from django.views import generic
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


@login_required(login_url='vendor:login')
@vendor_required
def add_products(request):
    if request.method == 'POST':
        form = ProductsAdd(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vendor:home')

    else:
        form = ProductsAdd()
    return render(request, 'vendor/add_products.html', {'form': form})


@login_required(login_url='vendor:login')
@vendor_required
def view_products(request):
    product_list = Product.objects.all().order_by('prod_name')

    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'vendor/view_products.html', {'products': products})


@login_required(login_url='vendor:login')
@vendor_required
def modify_products(request, id):
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        name = request.POST['prod_name']
        cat = request.POST['prod_cat']
        brand = request.POST['prod_brand']
        qty = request.POST['prod_qty']
        cost = request.POST['prod_cost']

        product.prod_name = name
        product.qty = qty
        product.cost = cost
        product.category.cat_name = cat
        product.brand = brand
        product.save()
        return redirect('vendor:view_products')

    return render(request, 'vendor/modify_product.html', {'product': product})


@login_required(login_url='vendor:login')
@vendor_required
def delete_product(request, id):
    product = Product.objects.get(pk=id)
    name = product.prod_name
    product.delete()
    return render(request, 'vendor/deleted.html', {'name': name})


@login_required(login_url='vendor:login')
@vendor_required
def view_orders(request):
    orders = Order.objects.filter(is_ordered=True)
    return render(request, 'vendor/show_orders.html', {'orders': orders})
