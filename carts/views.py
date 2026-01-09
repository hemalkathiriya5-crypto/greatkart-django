from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


@login_required
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variations = []

    if request.method == 'POST':
        for key in request.POST:
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variations.append(variation)
            except:
                pass

    cart, created = Cart.objects.get_or_create(
        user=request.user,
        is_ordered=False
    )

    cart_items = CartItem.objects.filter(cart=cart, product=product)

    # ✅ SAME PRODUCT EXISTS
    if cart_items.exists():
        for item in cart_items:
            existing_variations = list(item.variation.all())

            # ✅ SAME VARIATION → QUANTITY +
            if existing_variations == product_variations:
                item.quantity += 1
                item.save()
                return redirect('carts:cart')

    # ❌ SAME VARIATION NOT FOUND → NEW ITEM
    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=1
    )

    if product_variations:
        cart_item.variation.add(*product_variations)

    return redirect('carts:cart')


@login_required
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    cart = get_object_or_404(
        Cart,
        user=request.user,
        is_ordered=False
    )

    try:
        cart_item = CartItem.objects.get(
            cart=cart,
            product=product,
            id=cart_item_id
        )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except CartItem.DoesNotExist:
        pass

    return redirect('carts:cart')


@login_required
def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart__user=request.user,
        cart__is_ordered=False
    )
    cart_item.delete()
    return redirect('carts:cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(
        cart__user=request.user,
        cart__is_ordered=False
    )

    total = 0
    quantity = 0

    for item in cart_items:
        total += item.product.price * item.quantity
        quantity += item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)
