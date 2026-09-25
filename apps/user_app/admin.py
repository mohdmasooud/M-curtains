from django.contrib import admin
from .models import (
    UserProfile, ShippingAddress, Category, Fabric, RoomType, 
    PleatType, LiningType, Product, ProductImage, ProductReview, 
    Coupon, Order, OrderItem
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'base_price', 'discount_price', 'stock_quantity', 'is_available']
    list_filter = ['category', 'is_available', 'is_featured', 'is_bestseller']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(UserProfile)
admin.site.register(ShippingAddress)
admin.site.register(Fabric)
admin.site.register(RoomType)
admin.site.register(PleatType)
admin.site.register(LiningType)
admin.site.register(ProductImage)
admin.site.register(ProductReview)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(OrderItem)
