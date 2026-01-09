from .models import Cart
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
    
