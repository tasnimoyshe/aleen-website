from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, CustomizationRequest


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'custom_item_name', 'quantity', 'unit_price', 'unit_cost')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_type', 'customer_name', 'phone', 'area', 'total_amount', 'status', 'created_at')
    list_filter = ('order_type', 'status', 'created_at')
    list_editable = ('status',)
    search_fields = ('customer_name', 'phone', 'area', 'address')
    inlines = [OrderItemInline]


@admin.register(CustomizationRequest)
class CustomizationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'customer_name', 'phone', 'is_contacted', 'created_at')
    list_filter = ('is_contacted', 'created_at')
    list_editable = ('is_contacted',)
    search_fields = ('customer_name', 'phone', 'address', 'description')
    readonly_fields = ('image_preview', 'created_at')

    def image_preview(self, obj):
        if obj.reference_image:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="height:64px; width:64px; object-fit:cover; border-radius:8px; border:1px solid #E3D6BF;" /></a>',
                obj.reference_image.url
            )
        return "No image"
    image_preview.short_description = "Reference Photo"