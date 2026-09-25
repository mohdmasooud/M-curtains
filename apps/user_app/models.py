import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# --- User & Address Models ---

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='India')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    recipient_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    apartment_suite = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Shipping Addresses'
        ordering = ['-is_default', '-created_at']

    def save(self, *args, **kwargs):
        if self.is_default:
            ShippingAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.recipient_name} - {self.street_address}, {self.city}"


# --- Catalog & Customization Models ---

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='categories/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, help_text="Direct URL fallback for category banner")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return '/static/images/category-placeholder.jpg'


class Fabric(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    composition = models.CharField(max_length=255, blank=True, help_text="e.g. 100% Pure Velvet, 80% Linen 20% Cotton")
    care_instructions = models.TextField(blank=True, default="Dry clean recommended. Gentle iron on reverse.")

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PleatType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    fullness_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('1.00'))
    extra_cost = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class LiningType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    extra_cost = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    rooms = models.ManyToManyField(RoomType, blank=True, related_name='products')
    
    short_description = models.CharField(max_length=300, help_text="One-liner summary for catalog cards")
    description = models.TextField(help_text="Detailed product information, weave style, light control")
    
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base price for standard 140cm x 220cm panel")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Discounted price if on sale")
    
    stock_quantity = models.PositiveIntegerField(default=50)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    
    blackout_percentage = models.PositiveIntegerField(
        default=85,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="0% (Sheer) to 100% (Total Blackout)"
    )
    
    default_width_cm = models.PositiveIntegerField(default=140, help_text="Standard panel width in cm")
    default_drop_cm = models.PositiveIntegerField(default=225, help_text="Standard panel drop length in cm")
    
    color_name = models.CharField(max_length=50, default='Champagne Gold')
    color_hex = models.CharField(max_length=20, default='#C5A880', help_text="Hex code e.g. #C5A880 for swatches")
    
    primary_image = models.FileField(upload_to='products/', blank=True, null=True)
    primary_image_url = models.URLField(max_length=500, blank=True, help_text="Curated image fallback")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        if self.discount_price and self.discount_price < self.base_price:
            return self.discount_price
        return self.base_price

    @property
    def discount_percent(self):
        if self.discount_price and self.discount_price < self.base_price:
            diff = self.base_price - self.discount_price
            return int(round((diff / self.base_price) * 100))
        return 0

    @property
    def display_image(self):
        if self.primary_image:
            try:
                return self.primary_image.url
            except Exception:
                pass
        if self.primary_image_url:
            return self.primary_image_url
        return '/static/images/curtain_gold_velvet.jpg'

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg = sum(r.rating for r in reviews) / reviews.count()
            return round(avg, 1)
        return 4.8

    @property
    def review_count(self):
        return self.reviews.count()

    def calculate_custom_price(self, width_cm=None, drop_cm=None, pleat=None, lining=None):
        """Calculates dynamic price according to width, drop, pleat multiplier, and lining in INR."""
        width = Decimal(str(width_cm or self.default_width_cm))
        drop = Decimal(str(drop_cm or self.default_drop_cm))
        base_std_area = Decimal(str(self.default_width_cm * self.default_drop_cm))
        custom_area = width * drop
        
        area_ratio = custom_area / base_std_area
        price = self.current_price * (Decimal('0.5') + (Decimal('0.5') * area_ratio))
        
        if pleat and hasattr(pleat, 'extra_cost'):
            price += pleat.extra_cost
            
        if lining and hasattr(lining, 'extra_cost'):
            price += lining.extra_cost
            
        return round(price, 2)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.FileField(upload_to='products/gallery/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return '/static/images/product-placeholder.jpg'


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=150, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"


# --- Cart & Coupon Models ---

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Discount percentage (e.g. 15 for 15% off)"
    )
    min_purchase_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Minimum subtotal required to apply coupon"
    )
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% OFF)"

    def is_valid_for_amount(self, amount):
        if not self.is_active:
            return False, "This coupon is no longer active."
        if amount < self.min_purchase_amount:
            return False, f"Minimum purchase of ₹{self.min_purchase_amount} required for this coupon."
        return True, "Valid coupon"


# --- Order & Fulfillment Models ---

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending Confirmation'),
        ('Confirmed', 'Order Confirmed'),
        ('Tailoring', 'In Custom Tailoring'),
        ('Shipped', 'Shipped / In Transit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('card', 'Credit / Debit Card'),
        ('cod', 'Cash on Delivery'),
        ('upi', 'Instant UPI / Net Banking'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    )

    order_number = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Customer Details
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    
    # Shipping Address
    street_address = models.CharField(max_length=255)
    apartment_suite = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    
    order_notes = models.TextField(blank=True, help_text="Special instructions for curtain hanging or tailoring")
    
    # Financials (in ₹)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment & Fulfillment
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='card')
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    tracking_number = models.CharField(max_length=100, blank=True)
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"LX-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} ({self.full_name})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def status_step(self):
        mapping = {
            'Pending': 1,
            'Confirmed': 2,
            'Tailoring': 3,
            'Shipped': 4,
            'Delivered': 5,
            'Cancelled': 0,
        }
        return mapping.get(self.status, 1)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    product_image_url = models.URLField(max_length=500, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Custom specs
    width_cm = models.PositiveIntegerField(default=140)
    drop_cm = models.PositiveIntegerField(default=225)
    pleat_name = models.CharField(max_length=100, default='Standard Eyelet')
    lining_name = models.CharField(max_length=100, default='Standard Unlined')

    def __str__(self):
        return f"{self.quantity}x {self.product_name} ({self.width_cm}x{self.drop_cm}cm)"
