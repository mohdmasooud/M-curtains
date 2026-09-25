from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.user_app.models import (
    UserProfile, ShippingAddress, Category, Fabric, RoomType, 
    PleatType, LiningType, Product, ProductImage, ProductReview, 
    Coupon, Order, OrderItem
)
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Seeds initial realistic curtain categories, products, fabrics, users, coupons, and orders.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding LuxeDrape Curtain Shop Database (user_app)..."))

        # 1. Create Superuser / Admin
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@luxedrape.com', 'admin123')
            admin_user.first_name = 'Eleanor'
            admin_user.last_name = 'Vance (Admin)'
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("[OK] Admin user created: admin / admin123"))
        else:
            admin_user = User.objects.get(username='admin')

        # 2. Create Demo Customer
        if not User.objects.filter(username='customer').exists():
            customer = User.objects.create_user('customer', 'customer@example.com', 'customer123')
            customer.first_name = 'Sophia'
            customer.last_name = 'Montgomery'
            customer.save()
            
            # Create Customer Shipping Address
            ShippingAddress.objects.create(
                user=customer,
                recipient_name="Sophia Montgomery",
                phone_number="+91 98765 43210",
                street_address="742 Evergreen Terrace",
                apartment_suite="Penthouse 4B",
                city="Mumbai",
                state="Maharashtra",
                postal_code="400001",
                country="India",
                is_default=True
            )
            self.stdout.write(self.style.SUCCESS("[OK] Demo Customer created: customer / customer123"))
        else:
            customer = User.objects.get(username='customer')

        # 3. Create Pleat Types
        pleat_data = [
            ('Eyelet / Grommet', 'Modern metal ring eyelets that glide smoothly over curtain rods.', Decimal('1.00'), Decimal('0.00')),
            ('Pinch Pleat (Double / Triple)', 'Classic, tailored header with permanently stitched folds for luxurious full drape.', Decimal('1.25'), Decimal('250.00')),
            ('Pencil Pleat', 'Traditional tightly gathered header resembling a row of pencils side-by-side.', Decimal('1.15'), Decimal('150.00')),
            ('Inverted Box Pleat', 'Clean architectural flat surface with hidden reverse deep pleats for a minimalist look.', Decimal('1.20'), Decimal('200.00')),
            ('Wave Pleat / S-Fold', 'Continuous flowing S-curve wave effect from ceiling to floor track.', Decimal('1.30'), Decimal('350.00')),
        ]
        pleats = {}
        for name, desc, mult, cost in pleat_data:
            p, _ = PleatType.objects.get_or_create(name=name, defaults={'description': desc, 'fullness_multiplier': mult, 'extra_cost': cost})
            pleats[name] = p
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(pleats)} Pleat Types ready."))

        # 4. Create Lining Types
        lining_data = [
            ('Standard Unlined (Natural Drape)', 'Light single-layer drape preserving the original translucent hand-feel of the woven fabric.', Decimal('0.00')),
            ('Light-Filtering Satin Lining', 'Soft white sateen lining protecting curtain fabric from UV damage while diffusing harsh sunlight.', Decimal('120.00')),
            ('100% Total Blackout White Lining', '3-Pass magnetic blackout thermal coating blocking 100% of light and reducing outdoor sound by up to 40%.', Decimal('220.00')),
            ('Acoustic Interlining (Thermal + Heavy Sound Block)', 'Plump felt core sandwiched between face fabric and lining for supreme acoustic dampening & draft insulation.', Decimal('380.00')),
        ]
        linings = {}
        for name, desc, cost in lining_data:
            l, _ = LiningType.objects.get_or_create(name=name, defaults={'description': desc, 'extra_cost': cost})
            linings[name] = l
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(linings)} Lining Types ready."))

        # 5. Create Categories
        categories_data = [
            ('Luxury Velvet Drapes', 'luxury-velvet-drapes', 'Opulent heavy velvet with deep pile, sound absorption, and dramatic European theater elegance.', 'https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80', True),
            ('French Washed Linen', 'french-washed-linen', 'Relaxed, organic pure European flax linen creating effortless airy textures and light diffusion.', 'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=800&q=80', True),
            ('Total Blackout Sanctuary', 'total-blackout-sanctuary', 'Architectural blackout curtains offering 100% darkness, complete UV isolation, and acoustic serenity.', 'https://images.unsplash.com/photo-1540518614846-7ede433c4550?auto=format&fit=crop&w=800&q=80', True),
            ('Sheer Voile & Chiffon', 'sheer-voile-chiffon', 'Whisper-light ethereal drapery softening daylight while maintaining privacy and exterior garden views.', 'https://images.unsplash.com/photo-1616046229478-9901c5536a45?auto=format&fit=crop&w=800&q=80', True),
            ('Acoustic & Thermal Wool', 'acoustic-thermal-wool', 'Dense wool-blend architectural draping engineered for sound studios, grand halls, and draft prevention.', 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=800&q=80', False),
            ('Smart Motorized Ensembles', 'smart-motorized-ensembles', 'Somfy and Zigbee-integrated automated drape tracks custom fitted with silent whisper motors.', 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=800&q=80', False),
        ]
        categories = {}
        for name, slug, desc, img_url, feat in categories_data:
            c, _ = Category.objects.get_or_create(
                slug=slug, 
                defaults={'name': name, 'description': desc, 'image_url': img_url, 'is_featured': feat}
            )
            categories[slug] = c
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(categories)} Categories ready."))

        # 6. Create Fabrics
        fabrics_data = [
            ('Imperial Silk Velvet (420 GSM)', 'imperial-silk-velvet', '80% Rayon, 20% Mulberry Silk. 420 GSM heavy weight.'),
            ('Normandy Pure Washed Linen (280 GSM)', 'normandy-pure-washed-linen', '100% French Flax. Pre-washed for soft crumpled texture.'),
            ('Triple-Weave Obsidian Blackout (350 GSM)', 'triple-weave-obsidian-blackout', '100% High-Density Polyester with bonded blackout yarn.'),
            ('Belgian Textured Bouclé (450 GSM)', 'belgian-textured-boucle', '55% Wool, 30% Acrylic, 15% Cotton. Tactile nubby weave.'),
            ('Gossamer Cotton Voile (90 GSM)', 'gossamer-cotton-voile', '100% Organic Long-Staple Combed Cotton. Translucent.'),
        ]
        fabrics = {}
        for name, slug, comp in fabrics_data:
            f, _ = Fabric.objects.get_or_create(slug=slug, defaults={'name': name, 'composition': comp})
            fabrics[slug] = f
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(fabrics)} Fabrics ready."))

        # 7. Create Room Types
        room_data = [
            ('Living Room', 'living-room'),
            ('Master Bedroom', 'master-bedroom'),
            ('Dining Salon', 'dining-salon'),
            ('Home Cinema & Studio', 'home-cinema-studio'),
            ('Executive Study', 'executive-study'),
        ]
        rooms = {}
        for name, slug in room_data:
            r, _ = RoomType.objects.get_or_create(slug=slug, defaults={'name': name})
            rooms[slug] = r
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(rooms)} Room Types ready."))

        # 8. Create Rich Luxury Curtain Products
        product_data = [
            {
                'name': 'Champagne Gold Heavy Velvet Drape',
                'slug': 'champagne-gold-heavy-velvet-drape',
                'category': categories['luxury-velvet-drapes'],
                'fabric': fabrics['imperial-silk-velvet'],
                'rooms': [rooms['living-room'], rooms['dining-salon']],
                'short_description': 'Opulent 420 GSM silk-blend velvet with luminous golden sheen and acoustic dampening.',
                'description': 'Elevate your grand reception room or master suite with our signature Champagne Gold Heavy Velvet Drape. Woven with an authentic silk-rayon blend, this curtain catches daylight with soft incandescent highlights and cascades into deep tailored folds. Provides 95% light blocking and 35% sound dampening.',
                'base_price': Decimal('149.00'),
                'discount_price': Decimal('129.00'),
                'stock_quantity': 45,
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'blackout_percentage': 95,
                'default_width_cm': 140,
                'default_drop_cm': 240,
                'color_name': 'Champagne Gold',
                'color_hex': '#C5A880',
                'primary_image': 'products/curtain_gold_velvet.jpg',
                'primary_image_url': '/static/images/curtain_gold_velvet.jpg',
            },
            {
                'name': 'Heritage Emerald Silk Velvet Drape',
                'slug': 'heritage-emerald-silk-velvet-drape',
                'category': categories['luxury-velvet-drapes'],
                'fabric': fabrics['imperial-silk-velvet'],
                'rooms': [rooms['living-room'], rooms['master-bedroom'], rooms['executive-study']],
                'short_description': 'Dramatic deep jewel emerald velvet engineered for timeless stately interiors.',
                'description': 'A masterpiece of European mill craftsmanship, the Heritage Emerald Velvet drape brings royal depth to salon windows. Dense 420 GSM pile ensures insulation during winter chills and optimal daylight reduction.',
                'base_price': Decimal('159.00'),
                'discount_price': None,
                'stock_quantity': 30,
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': True,
                'blackout_percentage': 95,
                'default_width_cm': 140,
                'default_drop_cm': 250,
                'color_name': 'Heritage Emerald',
                'color_hex': '#0F4C3A',
                'primary_image': 'products/curtain_emerald_velvet.jpg',
                'primary_image_url': '/static/images/curtain_emerald_velvet.jpg',
            },
            {
                'name': 'Nordic Pure Washed Linen Panel',
                'slug': 'nordic-pure-washed-linen-panel',
                'category': categories['french-washed-linen'],
                'fabric': fabrics['normandy-pure-washed-linen'],
                'rooms': [rooms['living-room'], rooms['master-bedroom'], rooms['dining-salon']],
                'short_description': '100% French flax linen pre-washed with pumice stone for relaxed organic luxury.',
                'description': 'Handcrafted from Normandy flax, this washed linen drape breathes with natural slub irregularities that celebrate artisanal texture. Floods rooms with soft, diffused golden hour sunlight.',
                'base_price': Decimal('125.00'),
                'discount_price': Decimal('115.00'),
                'stock_quantity': 60,
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'blackout_percentage': 45,
                'default_width_cm': 145,
                'default_drop_cm': 230,
                'color_name': 'Natural Flax Oat',
                'color_hex': '#E3DAC9',
                'primary_image': 'products/curtain_nordic_linen.jpg',
                'primary_image_url': '/static/images/curtain_nordic_linen.jpg',
            },
            {
                'name': 'Midnight Eclipse 100% Total Blackout',
                'slug': 'midnight-eclipse-100-total-blackout',
                'category': categories['total-blackout-sanctuary'],
                'fabric': fabrics['triple-weave-obsidian-blackout'],
                'rooms': [rooms['master-bedroom'], rooms['home-cinema-studio']],
                'short_description': 'Engineered triple-pass blackout drape guaranteeing zero light bleed for deep restorative sleep.',
                'description': 'Designed specifically for light-sensitive sleepers and home cinema suites, the Midnight Eclipse combines a smooth matte architectural twill face with bonded polymer micro-coating that eliminates 100% of incoming light.',
                'base_price': Decimal('119.00'),
                'discount_price': Decimal('109.00'),
                'stock_quantity': 80,
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'blackout_percentage': 100,
                'default_width_cm': 140,
                'default_drop_cm': 225,
                'color_name': 'Obsidian Navy',
                'color_hex': '#1E293B',
                'primary_image': 'products/curtain_blackout_navy.jpg',
                'primary_image_url': '/static/images/curtain_blackout_navy.jpg',
            },
            {
                'name': 'Aura Gossamer Translucent Voile',
                'slug': 'aura-gossamer-translucent-voile',
                'category': categories['sheer-voile-chiffon'],
                'fabric': fabrics['gossamer-cotton-voile'],
                'rooms': [rooms['living-room'], rooms['dining-salon']],
                'short_description': 'Featherlight combed cotton sheer creating ethereal daylight diffusion with privacy.',
                'description': 'Gently filters strong glare while allowing natural air circulation and outside sightlines. Perfect when paired with our heavy velvet drapes on a dual curtain track system.',
                'base_price': Decimal('65.00'),
                'discount_price': Decimal('55.00'),
                'stock_quantity': 100,
                'is_featured': False,
                'is_bestseller': False,
                'is_new_arrival': True,
                'blackout_percentage': 15,
                'default_width_cm': 150,
                'default_drop_cm': 240,
                'color_name': 'Pure Alabaster White',
                'color_hex': '#F8F9FA',
                'primary_image': 'products/curtain_nordic_linen.jpg',
                'primary_image_url': '/static/images/curtain_nordic_linen.jpg',
            },
            {
                'name': 'Somfy Wave Motorized Linen Ensemble',
                'slug': 'somfy-wave-motorized-linen-ensemble',
                'category': categories['smart-motorized-ensembles'],
                'fabric': fabrics['normandy-pure-washed-linen'],
                'rooms': [rooms['living-room'], rooms['master-bedroom'], rooms['home-cinema-studio']],
                'short_description': 'Automated motorized S-wave curtain with ultra-quiet motor, remote control & smart home sync.',
                'description': 'Experience the pinnacle of modern luxury living. Operates with Apple HomeKit, Google Home, and Alexa or the included minimalist brushed brass wall remote.',
                'base_price': Decimal('299.00'),
                'discount_price': Decimal('269.00'),
                'stock_quantity': 25,
                'is_featured': True,
                'is_bestseller': False,
                'is_new_arrival': True,
                'blackout_percentage': 75,
                'default_width_cm': 200,
                'default_drop_cm': 260,
                'color_name': 'Mineral Warm Grey',
                'color_hex': '#94A3B8',
                'primary_image': 'products/curtain_blackout_navy.jpg',
                'primary_image_url': '/static/images/curtain_blackout_navy.jpg',
            },
        ]

        created_products = []
        for pdata in product_data:
            rooms_list = pdata.pop('rooms')
            p, created = Product.objects.get_or_create(slug=pdata['slug'], defaults=pdata)
            p.rooms.set(rooms_list)
            created_products.append(p)
            
            # Add gallery images
            if created:
                ProductImage.objects.create(
                    product=p,
                    image_url=p.primary_image_url,
                    alt_text=f"{p.name} Primary View",
                    is_primary=True
                )
                ProductImage.objects.create(
                    product=p,
                    image_url='https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80',
                    alt_text=f"{p.name} Close-up Weave Detail",
                    is_primary=False
                )
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(created_products)} Curtains created with gallery images."))

        # 9. Create Product Reviews
        reviews_data = [
            ('Sophia Montgomery', 5, 'Unbelievable tailoring and drape weight!', 'The champagne gold velvet looks like it belongs in a Versailles palace. The wave pleat is crisp and flawless.'),
            ('Marcus Vance', 5, 'Completely dark bedroom at noon.', 'I work night shifts and this 100% blackout curtain is the best investment I have made in years. Zero light bleed at seams.'),
            ('Claire Danvers', 4, 'Bespoke fit was exact to 0.5 cm.', 'Used the online calculator and entered custom drop 242 cm. It arrived floating precisely 1.5 cm above our hardwood floor.'),
        ]
        for author_name, rating, title, comment in reviews_data:
            ProductReview.objects.get_or_create(
                product=created_products[0],
                user=customer,
                title=title,
                defaults={'rating': rating, 'comment': comment}
            )
        self.stdout.write(self.style.SUCCESS("[OK] Authentic client reviews attached."))

        # 10. Create Coupons
        coupon_data = [
            ('WELCOME10', 10, Decimal('500.00')),
            ('LUXE20', 20, Decimal('2000.00')),
            ('CURTAINVIP', 25, Decimal('3500.00')),
        ]
        for code, disc, min_spend in coupon_data:
            Coupon.objects.get_or_create(
                code=code,
                defaults={
                    'discount_percentage': disc,
                    'min_purchase_amount': min_spend,
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS("[OK] Active coupons created: WELCOME10 (10%), LUXE20 (20%), CURTAINVIP (25%)"))

        # 11. Create Sample Orders for Admin Dashboard Analytics
        order_specs = [
            ('Sophia Montgomery', 'customer@example.com', '+91 98765 43210', 'Delivered', 'Paid', 'card', 'LX-FEDEX-901823', Decimal('3880.00'), Decimal('200.00'), Decimal('0.00'), Decimal('184.00'), Decimal('3864.00')),
            ('Arthur Pendelton', 'arthur.p@gmail.com', '+91 98765 12345', 'Shipped', 'Paid', 'card', 'LX-UPS-449102', Decimal('2690.00'), Decimal('0.00'), Decimal('0.00'), Decimal('134.50'), Decimal('2824.50')),
            ('Victoria Sterling', 'v.sterling@vancemedia.com', '+91 98765 87654', 'Tailoring', 'Paid', 'upi', '', Decimal('4470.00'), Decimal('447.00'), Decimal('0.00'), Decimal('201.15'), Decimal('4224.15')),
            ('Marcus Holloway', 'marcus.h@gmail.com', '+91 98765 31299', 'Confirmed', 'Pending', 'cod', '', Decimal('1490.00'), Decimal('0.00'), Decimal('150.00'), Decimal('74.50'), Decimal('1714.50')),
            ('Genevieve Dupont', 'g.dupont@architects.fr', '+91 98765 67811', 'Pending', 'Pending', 'card', '', Decimal('6380.00'), Decimal('638.00'), Decimal('0.00'), Decimal('287.10'), Decimal('6029.10')),
        ]

        for i, (fname, email, phone, status, pay_status, pay_method, track, sub, disc, ship, tax, tot) in enumerate(order_specs):
            order, created = Order.objects.get_or_create(
                order_number=f"LX-DEMO-{1001 + i}",
                defaults={
                    'user': customer if i % 2 == 0 else None,
                    'full_name': fname,
                    'email': email,
                    'phone': phone,
                    'street_address': f"{100 + i * 15} Royal Avenue",
                    'apartment_suite': 'Suite 12',
                    'city': 'Mumbai',
                    'state': 'Maharashtra',
                    'postal_code': '400001',
                    'country': 'India',
                    'subtotal': sub,
                    'discount_amount': disc,
                    'shipping_fee': ship,
                    'tax_amount': tax,
                    'total_amount': tot,
                    'payment_method': pay_method,
                    'payment_status': pay_status,
                    'status': status,
                    'tracking_number': track,
                    'order_notes': 'Custom tailored floor-to-ceiling fit for 9ft ceiling drop.',
                    'admin_notes': 'Measurement specs confirmed with client via email.'
                }
            )
            if created and len(created_products) > i:
                prod = created_products[i]
                OrderItem.objects.create(
                    order=order,
                    product=prod,
                    product_name=prod.name,
                    product_image_url=prod.display_image,
                    unit_price=prod.current_price,
                    quantity=2,
                    total_price=prod.current_price * 2,
                    width_cm=180,
                    drop_cm=260,
                    pleat_name='Pinch Pleat (Double / Triple)',
                    lining_name='100% Total Blackout White Lining',
                )

        self.stdout.write(self.style.SUCCESS("[OK] Sample Orders created for Analytics & Dashboard."))
        self.stdout.write(self.style.SUCCESS("[SUCCESS] LUXEDRAPE USER_APP DATABASE SEEDING COMPLETED SUCCESSFULLY!"))
