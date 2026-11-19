import os
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from .utils import process_hero_bouquet


class BannerAd(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, help_text="ব্যানারে ক্লিক করলে যে লিংকে যাবে (অপশনাল)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # সর্বোচ্চ ৩টি অ্যাক্টিভ ব্যানার চেক
        if self.is_active:
            active_count = BannerAd.objects.filter(is_active=True).exclude(pk=self.pk).count()
            if active_count >= 3:
                raise ValidationError("সর্বোচ্চ ৩টি অ্যাক্টিভ ব্যানার অ্যাড পোস্ট করা যাবে। নতুন ব্যানার দিতে হলে আগের একটি বন্ধ করুন।")

    def __str__(self):
        return self.title


class Review(models.Model):
    SOURCE_CHOICES = [
        ('WEBSITE', 'Website Customer'),
        ('IN_STORE', 'In-Store Customer'),
        ('SOCIAL', 'Social Media'),
    ]

    customer_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='WEBSITE')
    is_approved = models.BooleanField(default=False, help_text="অ্যাপ্রুভ করলে ল্যান্ডিং পেজে শো করবে")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"


class StoreMemory(models.Model):
    title = models.CharField(max_length=150)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='store_memories/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Store Memories"

    def __str__(self):
        return self.title


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)  # যেমন: VALENTINE20
    discount_percent = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    valid_until = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"


class SiteSettings(models.Model):
    show_visitor_count = models.BooleanField(default=True, help_text="ওয়েবসাইটে লাইভ ভিজিটর কাউন্ট দেখাবেন?")
    default_shipping_fee = models.DecimalField(max_digits=8, decimal_places=2, default=80.00)
    membership_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    membership_benefits = models.TextField(default="সকল অর্ডারে ১০% ডিসকাউন্ট এবং প্রায়োরিটি ডেলিভারি।")
    quick_membership_phone = models.CharField(max_length=20, default="+8801XXXXXXXXX")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Aleen Site Settings"


class HeroSlide(models.Model):
    name = models.CharField(max_length=150, help_text="ফুল বা বুকের নাম (অ্যাডমিন প্যানেলে চেনার জন্য)")
    image = models.ImageField(
        upload_to='hero_flowers/',
        help_text="যেকোনো বুকের ছবি আপলোড করুন — ব্যাকগ্রাউন্ড অটো রিমুভ হয়ে সমান সাইজে সেভ হবে"
    )
    left_description = models.TextField(help_text="বুকের বাম পাশের ডেসক্রিপশন")
    right_description = models.TextField(help_text="বুকের ডান পাশের ডেসক্রিপশন")
    display_order = models.PositiveIntegerField(default=0, help_text="যে ক্রমে দেখাবে (0, 1, 2...)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Hero Flower Slide"
        verbose_name_plural = "Hero Flower Slides"

    def save(self, *args, **kwargs):
        if self.image:
            is_new_upload = getattr(self.image, '_committed', True) is False
            not_cleaned_yet = not self.image.name.lower().endswith('_clean.png')

            if is_new_upload or not_cleaned_yet:
                processed_io, status_msg = process_hero_bouquet(self.image)
                print(f"[HeroSlide: {self.name}] {status_msg}")
                if processed_io:
                    base_name = os.path.splitext(os.path.basename(self.image.name))[0].replace('_clean', '')
                    new_filename = f"{base_name}_clean.png"
                    self.image.save(new_filename, ContentFile(processed_io.read()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name