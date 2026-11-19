import os
from django.contrib import admin, messages
from django.core.files.base import ContentFile
from .models import HeroSlide, BannerAd, Review, StoreMemory, Coupon, SiteSettings
from .utils import process_hero_bouquet


@admin.action(description="Remove Background & Uniform Resize (Selected Slides)")
def clean_and_resize_slides(modeladmin, request, queryset):
    success_count = 0
    for slide in queryset:
        if not slide.image:
            continue
        processed_io, status_msg = process_hero_bouquet(slide.image)
        if processed_io:
            base_name = os.path.splitext(os.path.basename(slide.image.name))[0].replace('_clean', '')
            new_filename = f"{base_name}_clean.png"
            slide.image.save(new_filename, ContentFile(processed_io.read()), save=False)
            super(HeroSlide, slide).save(update_fields=['image'])
            success_count += 1
        else:
            modeladmin.message_user(request, f"{slide.name}: {status_msg}", level=messages.ERROR)

    if success_count:
        modeladmin.message_user(
            request,
            f"{success_count}টি ফুলের ব্যাকগ্রাউন্ড রিমুভ ও সাইজ সমান করা হয়েছে!",
            level=messages.SUCCESS
        )


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_active', 'created_at')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
    actions = [clean_and_resize_slides]


admin.site.register(BannerAd)
admin.site.register(Review)
admin.site.register(StoreMemory)
admin.site.register(Coupon)
admin.site.register(SiteSettings)