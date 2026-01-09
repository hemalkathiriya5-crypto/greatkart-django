from .models import CartItem

def counter(request):
    cart_count = 0

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(
            cart__user=request.user,
            cart__is_ordered=False
        )

        for item in cart_items:
            cart_count += item.quantity

    return {
        'cart_count': cart_count
    }
