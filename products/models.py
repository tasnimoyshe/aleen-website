from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # যেমন: Loose Blooms, Flower Bags, Flower Bouquets
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        help_text="সাব-ক্যাটাগরি হলে মেইন ক্যাটাগরি সিলেক্ট করুন (যেমন: Cone-এর জন্য Artificial Blooms)"
    )
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='products/')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="কেনা খরচ (প্রফিট হিসাবের জন্য)")
    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Regular Price",
        help_text="নরমাল বা আসল দাম (যেমন: 3000)"
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Discount Price (Present)",
        help_text="ডিসকাউন্ট দিলে বর্তমান দাম এখানে দিন (যেমন: 2600)। ডিসকাউন্ট না থাকলে খালি রাখুন।"
    )
    stock_qty = models.PositiveIntegerField(default=0)
    short_description = models.TextField(blank=True)
    story_description = models.TextField(
        blank=True,
        help_text="এই ফুলটি কীসের প্রতীক এবং কাদের দেওয়া উচিত (হিরো সেকশন ও ডিটেইলসে দেখাবে)"
    )
    is_hero_featured = models.BooleanField(default=False, help_text="হিরো সেকশনের ৩০-সেকেন্ড অ্যানিমেশনে দেখাবেন?")
    is_available = models.BooleanField(default=True)
    sales_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_in_stock(self):
        return self.stock_qty > 0 and self.is_available

    @property
    def has_discount(self):
        return bool(self.discount_price and self.discount_price < self.selling_price)

    @property
    def current_price(self):
        return self.discount_price if self.has_discount else self.selling_price

    @property
    def profit_per_unit(self):
        return self.current_price - self.cost_price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name