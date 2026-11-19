from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def shop(request):
    categories = Category.objects.all()
    selected_slug = request.GET.get('category', '')
    search_query = request.GET.get('q', '').strip()

    products = Product.objects.filter(is_available=True).select_related('category').order_by('-created_at')
    active_category = None

    if selected_slug:
        active_category = get_object_or_404(Category, slug=selected_slug)
        products = products.filter(category=active_category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category,
        'search_query': search_query,
    }
    return render(request, 'products/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)