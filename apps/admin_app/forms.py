from django import forms
from apps.user_app.models import Product, Category, Fabric, Order, Coupon

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'fabric', 'rooms', 'short_description', 
            'description', 'base_price', 'discount_price', 'stock_quantity', 
            'blackout_percentage', 'default_width_cm', 'default_drop_cm', 
            'color_name', 'color_hex', 'primary_image', 'primary_image_url', 
            'is_available', 'is_featured', 'is_bestseller', 'is_new_arrival'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Curtain Model Name'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'fabric': forms.Select(attrs={'class': 'form-select'}),
            'rooms': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'One-line overview for catalog cards'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed weaving specifications & care'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Optional sale price'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'blackout_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'default_width_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'default_drop_cm': forms.NumberInput(attrs={'class': 'form-control'}),
            'color_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Champagne Gold'}),
            'color_hex': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '#C5A880'}),
            'primary_image': forms.FileInput(attrs={'class': 'form-control'}),
            'primary_image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_bestseller': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_new_arrival': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image', 'image_url', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-generated or custom slug'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short category narrative'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FabricAdminForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = ['name', 'slug', 'composition', 'care_instructions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'composition': forms.TextInput(attrs={'class': 'form-control'}),
            'care_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'tracking_number', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. FEDEX-901823'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Internal notes on custom tailoring & client communication'}),
        }


class CouponAdminForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'min_purchase_amount', 'is_active']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PROMO20'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '100'}),
            'min_purchase_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
