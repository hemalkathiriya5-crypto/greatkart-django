from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator  # ✅ fixed typo


def store(request, category_slug=None):
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        # Pagination for category products
        paginator = Paginator(products, 3)  # 6 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)  # 6 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    # ✅ Check for products already in cart
    in_cart_products = []
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user, cart__is_ordered=False)
        in_cart_products = [item.product.id for item in cart_items]

    context = {
        'products': paged_products,
        'product_count': products.count(),
        'categories': categories,
        'in_cart_products': in_cart_products,
    }
    return render(request, 'store/store.html', context)


def product_details(request, category_slug, product_slug):
    single_product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
        is_available=True
    )

    # ✅ Check if this single product is already in cart
    in_cart = False
    if request.user.is_authenticated:
        in_cart = CartItem.objects.filter(
            cart__user=request.user,
            cart__is_ordered=False,
            product=single_product
        ).exists()

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_details.html', context)


def search(request):
    keyword = request.GET.get('keyword')
    products = Product.objects.none()

    if keyword:
        products = Product.objects.filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword),
            is_available=True
        ).order_by('id')

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': products.count(),
    }
    return render(request, 'store/store.html', context)
