from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from products.models import Category, Product
from core.models import HeroSlide, BannerAd, Review, SiteSettings
from orders.models import OrderItem


def home(request):
    now = timezone.localtime(timezone.now())

    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('display_order', 'id')
    hero_slides_data = [
        {
            'name': slide.name,
            'image': slide.image.url if slide.image else '',
            'left_description': slide.left_description,
            'right_description': slide.right_description,
        }
        for slide in hero_slides
    ]

    active_banners = BannerAd.objects.filter(is_active=True).order_by('-created_at')[:3]
    categories = Category.objects.filter(parent__isnull=True).order_by('display_order')[:4]

    # চলতি মাসের অনলাইন + স্টোর সেল মিলিয়ে টপ ৮ প্রোডাক্ট (ক্যানসেল অর্ডার বাদে)
    monthly_top_rows = (
        OrderItem.objects.filter(
            order__created_at__year=now.year,
            order__created_at__month=now.month,
            product__isnull=False,
            product__is_available=True,
        )
        .exclude(order__status='CANCELLED')
        .values('product_id')
        .annotate(month_qty=Sum('quantity'))
        .order_by('-month_qty')[:8]
    )

    top_ids = [row['product_id'] for row in monthly_top_rows]
    product_map = Product.objects.in_bulk(top_ids)
    most_loved = [product_map[pid] for pid in top_ids if pid in product_map]

    # মাসের শুরুতে ৮টির কম ফুল বিক্রি হয়ে থাকলে বাকি জায়গা অল-টাইম বেস্টসেলার দিয়ে পূরণ করবে
    if len(most_loved) < 8:
        remaining = 8 - len(most_loved)
        fallback_products = list(
            Product.objects.filter(is_available=True)
            .exclude(id__in=top_ids)
            .order_by('-sales_count', '-created_at')[:remaining]
        )
        most_loved.extend(fallback_products)

    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:6]
    site_settings = SiteSettings.objects.first()

    context = {
        'hero_slides_data': hero_slides_data,
        'active_banners': active_banners,
        'categories': categories,
        'most_loved': most_loved,
        'current_month': now.strftime('%B'),
        'reviews': reviews,
        'site_settings': site_settings,
    }
    return render(request, 'core/home.html', context)