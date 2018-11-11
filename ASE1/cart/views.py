from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from cart.models import orderitem, order, Transaction
from vendor.models import Product
from customer.models import CustomerProfile
from cart.extra import generate_order_id
import datetime

# Create your views here.

def get_user_pending_order(request):
    user_profile = get_object_or_404(CustomerProfile, Customer=request.user)
    ord = order.objects.filter(owner=user_profile, is_ordered=False)
    if ord.exists():
        return ord[0]
    return 0



@login_required(login_url='customer:login')
def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(CustomerProfile, Customer=request.user)
    product = Product.objects.get(id=kwargs.get('item_id'))
    print("lshsldlbka")
    user_order, status = order.objects.get_or_create(owner=user_profile, is_ordered=False)

    if product in user_order.items.all():
        messages.info(request, 'Already in Cart')
        return redirect(reverse('customer:profile'))

    if status:
        ref_code = generate_order_id()
        order_item, status = orderitem.objects.get_or_create(product=product, ref_code=ref_code)
        user_order.items.add(order_item)
        user_order.ref_code = ref_code
        user_order.save()
    else:
        order_item, status = orderitem.objects.get_or_create(product=product, ref_code=user_order.ref_code)
        user_order.items.add(order_item)
        user_order.save()
    # return redirect(reverse('customer:items', kwargs={'pk': int(kwargs['cat_id'])}))

    return HttpResponse("")


@login_required(login_url='customer:login')
def delete_from_cart(request, item_id):
    item_to_delete = orderitem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
    return redirect(reverse('cart:order_summary'))


@login_required(login_url='customer:login')
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'ordre': existing_order
    }
    return render(request, 'cart/order_summary.html', context)


@login_required(login_url='customer:login')
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'ordre': existing_order
    }
    return render(request, 'cart/checkout.html', context)


@login_required()
def update_transaction_records(request):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    transaction = Transaction(profile=request.user.cus,
                              order_id=order_to_purchase.ref_code,
                              amount=order_to_purchase.get_cart_total(),
                              success=True)

    transaction.save()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('customer:profile'))
