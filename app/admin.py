from django.contrib import admin
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'discounted_price',
        'selling_price',
        'category',
        'product_image'
    ]

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
        list_display = [
        'id',
        'user',
        'locality',
        'city',
        'state',
        'zipcode'
    ]
        
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product_link", "quantity")

    def product_link(self, obj):
        if obj.product:
            app_label = obj.product._meta.app_label
            model_name = obj.product._meta.model_name
            link = reverse(
                f"admin:{app_label}_{model_name}_change",
                args=[obj.product.pk]
            )
            return format_html('<a href="{}">{}</a>', link, obj.product.title)
        return "-"

    product_link.short_description = "Product"

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
     list_display=["id","user","amount","razorpay_order_id","razorpay_payment_status","razorpay_payment_id","paid"]

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = [
        "id", "user", "customer_link", "product_link",
        "quantity", "ordered_date", "status", "payment_link"
    ]

    def customer_link(self, obj):
        if obj.customer:
            app_label = obj.customer._meta.app_label
            model_name = obj.customer._meta.model_name
            link = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.customer.pk])
            return format_html('<a href="{}">{}</a>', link, obj.customer.name)  # assuming Customer has `name` field
        return "-"

    def product_link(self, obj):
        if obj.product:
            app_label = obj.product._meta.app_label
            model_name = obj.product._meta.model_name
            link = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.product.pk])
            return format_html('<a href="{}">{}</a>', link, obj.product.title)
        return "-"

    def payment_link(self, obj):
        if obj.payment:
            app_label = obj.payment._meta.app_label
            model_name = obj.payment._meta.model_name
            link = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.payment.pk])
            return format_html('<a href="{}">{}</a>', link, obj.payment.razorpay_payment_id)
        return "-"

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=["id","user","product"]

admin.site.unregister(Group)