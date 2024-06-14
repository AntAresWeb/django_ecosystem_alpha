from products.models import ProductSet


def check_params_is_none(*args):
    return any([arg is None for arg in args])


def append_product(shopingcart, params):
    product = params.get('product', None)
    quantity = params.get('quantity', None)
    if check_params_is_none(product, quantity):
        return
    try:
        productset = ProductSet.objects.get(
            shoppingcart=shopingcart, product=product)
    except ProductSet.DoesNotExist:
        productset = ProductSet(
            shoppingcart=shopingcart,
            product=product,
            quantity=quantity)
        productset.save()


def change_product(shopingcart, params):
    product = params.get('product', None)
    quantity = params.get('quantity', None)
    if check_params_is_none(product, quantity):
        return
    try:
        productset = ProductSet.objects.get(
            shoppingcart=shopingcart, product=product)
        productset.quantity = quantity
        productset.save()
    except ProductSet.DoesNotExist:
        return


def delete_product(shopingcart, params):
    product = params.get('product', None)
    if check_params_is_none(product):
        return
    try:
        ProductSet.objects.get(
            shoppingcart=shopingcart, product=product).delete()
    except ProductSet.DoesNotExist:
        return
