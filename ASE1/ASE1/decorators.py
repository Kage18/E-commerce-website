from functools import wraps
from django.shortcuts import redirect


def customer_required(original_function):
    @wraps(original_function)
    def wrapper_function(*args, **kwargs):
        try:
            args[0].user.customerprofile
            return original_function(*args, **kwargs)
        except Exception as ex:
            if type(ex).__name__ == 'RelatedObjectDoesNotExist':
                print("Differentiated between a customer and a vendor")
                return redirect('customer:actor_authentication:login_all')

    return wrapper_function


def vendor_required(original_function):
    @wraps(original_function)
    def wrapper_function(*args, **kwargs):
        try:
            args[0].user.vendorprofile
            return original_function(*args, **kwargs)
        except Exception as ex:
            if type(ex).__name__ == 'RelatedObjectDoesNotExist':
                print("Differentiated between a customer and a vendor")
                return redirect('vendor:actor_authentication:login_all')

    return wrapper_function
