from decimal import Decimal
from .models import Product, Coupon, PleatType, LiningType

CART_SESSION_ID = 'luxedrape_cart'
COUPON_SESSION_ID = 'luxedrape_coupon_id'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
        
        # Load active coupon if stored
        coupon_id = self.session.get(COUPON_SESSION_ID)
        self.coupon = Coupon.objects.filter(id=coupon_id, is_active=True).first() if coupon_id else None

    def add(self, product, quantity=1, width_cm=None, drop_cm=None, pleat_id=None, lining_id=None, override_quantity=False):
        width = int(width_cm or product.default_width_cm)
        drop = int(drop_cm or product.default_drop_cm)
        pleat = PleatType.objects.filter(id=pleat_id).first() if pleat_id else None
        lining = LiningType.objects.filter(id=lining_id).first() if lining_id else None

        # Unique key based on customization specs
        item_key = f"{product.id}_{width}_{drop}_{pleat_id or 0}_{lining_id or 0}"
        
        # Calculate bespoke unit price
        unit_price = product.calculate_custom_price(width_cm=width, drop_cm=drop, pleat=pleat, lining=lining)

        if item_key not in self.cart:
            self.cart[item_key] = {
                'product_id': product.id,
                'quantity': 0,
                'unit_price': str(unit_price),
                'width_cm': width,
                'drop_cm': drop,
                'pleat_id': pleat.id if pleat else None,
                'pleat_name': pleat.name if pleat else 'Standard Eyelet',
                'lining_id': lining.id if lining else None,
                'lining_name': lining.name if lining else 'Standard Unlined',
            }

        if override_quantity:
            self.cart[item_key]['quantity'] = int(quantity)
        else:
            self.cart[item_key]['quantity'] += int(quantity)

        self.save()

    def update_quantity(self, item_key, quantity):
        if item_key in self.cart:
            qty = int(quantity)
            if qty > 0:
                self.cart[item_key]['quantity'] = qty
            else:
                self.remove(item_key)
            self.save()

    def remove(self, item_key):
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def save(self):
        self.session.modified = True

    def apply_coupon(self, coupon_code):
        coupon = Coupon.objects.filter(code__iexact=coupon_code.strip(), is_active=True).first()
        if not coupon:
            return False, "Invalid or expired promotional coupon code."
        
        subtotal = self.get_subtotal()
        valid, msg = coupon.is_valid_for_amount(subtotal)
        if not valid:
            return False, msg

        self.session[COUPON_SESSION_ID] = coupon.id
        self.coupon = coupon
        self.save()
        return True, f"Coupon '{coupon.code}' applied successfully ({coupon.discount_percentage}% OFF)!"

    def remove_coupon(self):
        if COUPON_SESSION_ID in self.session:
            del self.session[COUPON_SESSION_ID]
            self.coupon = None
            self.save()

    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}

        for key, item in self.cart.items():
            product = products.get(item['product_id'])
            if product:
                item_copy = item.copy()
                item_copy['item_key'] = key
                item_copy['product'] = product
                item_copy['unit_price'] = Decimal(item['unit_price'])
                item_copy['total_price'] = item_copy['unit_price'] * item['quantity']
                yield item_copy

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(item['unit_price']) * item['quantity'] for item in self.cart.values())

    def get_discount_amount(self):
        if self.coupon:
            subtotal = self.get_subtotal()
            valid, _ = self.coupon.is_valid_for_amount(subtotal)
            if valid:
                return round((subtotal * Decimal(str(self.coupon.discount_percentage))) / Decimal('100'), 2)
        return Decimal('0.00')

    def get_shipping_fee(self):
        subtotal = self.get_subtotal()
        if subtotal == 0 or subtotal >= Decimal('2000.00'):
            return Decimal('0.00')  # Free shipping above ₹2,000
        return Decimal('150.00')

    def get_tax_amount(self):
        taxable = max(Decimal('0.00'), self.get_subtotal() - self.get_discount_amount())
        return round(taxable * Decimal('0.05'), 2)

    def get_grand_total(self):
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        shipping = self.get_shipping_fee()
        tax = self.get_tax_amount()
        return max(Decimal('0.00'), subtotal - discount + shipping + tax)

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        if COUPON_SESSION_ID in self.session:
            del self.session[COUPON_SESSION_ID]
        self.save()
