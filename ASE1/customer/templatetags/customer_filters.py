from django import template
from vendor.models import VendorQty

register = template.Library()


@register.filter
def get_qty(stock):
    try:
        stock = int(stock)
    except ValueError:
        raise ValueError('Stock should be an integer!')
    if stock <= 10:
        return list(range(stock))
    else:
        return list(range(10))


@register.filter
def get_qty_number(item):
    ven = item.vendor.all()[0]
    ven_qty = VendorQty.objects.get(Vendor=ven, product=item.product)
    arr = get_qty(ven_qty.qty)
    return arr


@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price
