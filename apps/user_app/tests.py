import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.user_app.models import (
    Product, Category, Fabric, RoomType, PleatType, LiningType,
    Coupon, Order, OrderItem, ShippingAddress, UserProfile, ProductReview
)

class UserAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test customer and admin users
        self.customer = User.objects.create_user(
            username='testcustomer',
            email='testcustomer@example.com',
            password='TestPassword123!',
            first_name='Sophia',
            last_name='Montgomery'
        )
        
        self.category = Category.objects.create(
            name='Royal Velvet',
            slug='royal-velvet',
            description='Luxurious high pile velvet'
        )
        
        self.fabric = Fabric.objects.create(
            name='100% Pure Velvet',
            slug='pure-velvet',
            composition='100% Silk-Touch Velvet'
        )
        
        self.room = RoomType.objects.create(
            name='Master Suite',
            slug='master-suite'
        )
        
        self.pleat = PleatType.objects.create(
            name='French Pinch Pleat',
            slug='french-pinch-pleat',
            fullness_multiplier=Decimal('2.20'),
            extra_cost=Decimal('450.00')
        )
        
        self.lining = LiningType.objects.create(
            name='Thermal Blackout Lining',
            slug='thermal-blackout',
            extra_cost=Decimal('350.00')
        )
        
        self.product = Product.objects.create(
            name='Imperial Champagne Gold Velvet',
            slug='imperial-champagne-gold-velvet',
            category=self.category,
            fabric=self.fabric,
            short_description='Opulent velvet drapery panel',
            description='Heavy 420 GSM drape providing superior light blocking and acoustic insulation.',
            base_price=Decimal('2499.00'),
            discount_price=Decimal('2199.00'),
            stock_quantity=40,
            blackout_percentage=95,
            is_available=True,
            is_featured=True,
            is_bestseller=True,
            is_new_arrival=True,
            color_name='Champagne Gold',
            color_hex='#D4AF37'
        )
        self.product.rooms.add(self.room)
        
        self.coupon = Coupon.objects.create(
            code='LUXE20',
            discount_percentage=20,
            min_purchase_amount=Decimal('1000.00'),
            is_active=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CURTAINS')
        self.assertContains(response, 'Imperial Champagne Gold Velvet')
        self.assertContains(response, 'Royal Velvet')

    def test_product_catalog_and_filtering(self):
        # Product list
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

        # Filter by category
        response = self.client.get(reverse('products:product_list'), {'category': self.category.slug})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 1)

        # Filter by search
        response = self.client.get(reverse('products:product_list'), {'q': 'Champagne'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 1)

        # Sort by price
        response = self.client.get(reverse('products:product_list'), {'sort': 'price_low'})
        self.assertEqual(response.status_code, 200)

    def test_category_detail_view(self):
        response = self.client.get(reverse('products:category_detail', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, '₹')

    def test_live_search_api(self):
        response = self.client.get(reverse('products:search_api'), {'q': 'Champagne'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertTrue(len(data['results']) > 0)
        self.assertEqual(data['results'][0]['slug'], self.product.slug)

    def test_calculate_price_api(self):
        response = self.client.get(reverse('products:calculate_price_api', kwargs={'product_id': self.product.id}), {
            'width': '180',
            'drop': '250',
            'pleat_id': self.pleat.id,
            'lining_id': self.lining.id
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertGreater(data['calculated_price'], 0)
        self.assertIn('₹', data['formatted_price'])

    def test_interactive_tools_and_static_views(self):
        # Room visualizer
        response = self.client.get(reverse('core:room_visualizer'))
        self.assertEqual(response.status_code, 200)

        # Measurement guide
        response = self.client.get(reverse('core:measurement_guide'))
        self.assertEqual(response.status_code, 200)

        # About page
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)

        # Contact page GET and POST
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        
        post_response = self.client.post(reverse('core:contact'), {
            'name': 'Lord Sterling',
            'email': 'sterling@example.com',
            'message': 'Inquiring for custom villa drapery'
        })
        self.assertEqual(post_response.status_code, 302)

    def test_user_authentication_flow(self):
        # Register new customer
        reg_response = self.client.post(reverse('accounts:register'), {
            'username': 'newcustomer',
            'first_name': 'Eleanor',
            'last_name': 'Vane',
            'email': 'eleanor@example.com',
            'password': 'SecurePassword2026!',
            'confirm_password': 'SecurePassword2026!'
        })
        self.assertEqual(reg_response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newcustomer').exists())

        # Logout
        self.client.logout()

        # Login
        login_response = self.client.post(reverse('accounts:login'), {
            'username': 'newcustomer',
            'password': 'SecurePassword2026!'
        })
        self.assertEqual(login_response.status_code, 302)

        # Dashboard
        dash_response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(dash_response.status_code, 200)

        # Profile Update
        prof_response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Eleanor',
            'last_name': 'Vane-Hastings',
            'email': 'eleanor.updated@example.com',
            'phone_number': '+91 9876543210',
            'city': 'Mumbai',
            'country': 'India'
        })
        self.assertEqual(prof_response.status_code, 302)
        
        updated_user = User.objects.get(username='newcustomer')
        self.assertEqual(updated_user.last_name, 'Vane-Hastings')

    def test_address_crud(self):
        self.client.force_login(self.customer)
        
        # Add Address
        add_res = self.client.post(reverse('accounts:address_add'), {
            'recipient_name': 'Sophia Montgomery',
            'phone_number': '+91 9876500000',
            'street_address': '42 Marine Drive, Penthouse 12B',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400020',
            'country': 'India',
            'is_default': True
        })
        self.assertEqual(add_res.status_code, 302)
        self.assertEqual(ShippingAddress.objects.filter(user=self.customer).count(), 1)
        
        addr = ShippingAddress.objects.filter(user=self.customer).first()
        
        # Edit Address
        edit_res = self.client.post(reverse('accounts:address_edit', kwargs={'address_id': addr.id}), {
            'recipient_name': 'Lady Sophia Montgomery',
            'phone_number': '+91 9876500000',
            'street_address': '42 Marine Drive, Penthouse 12B',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400020',
            'country': 'India',
            'is_default': True
        })
        self.assertEqual(edit_res.status_code, 302)
        addr.refresh_from_db()
        self.assertEqual(addr.recipient_name, 'Lady Sophia Montgomery')

    def test_cart_and_checkout_flow(self):
        # 1. Add to Cart
        add_cart_res = self.client.post(reverse('cart:cart_add', kwargs={'product_id': self.product.id}), {
            'quantity': 2,
            'width_cm': 160,
            'drop_cm': 240,
            'pleat_type': self.pleat.id,
            'lining_type': self.lining.id
        })
        self.assertEqual(add_cart_res.status_code, 302)

        # 2. View Cart
        cart_page = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(cart_page.status_code, 200)
        self.assertContains(cart_page, self.product.name)

        # 3. Apply Coupon
        coupon_res = self.client.post(reverse('cart:coupon_apply'), {
            'coupon_code': 'LUXE20'
        })
        self.assertEqual(coupon_res.status_code, 302)

        # 4. Checkout GET
        checkout_page = self.client.get(reverse('orders:checkout'))
        self.assertEqual(checkout_page.status_code, 200)

        # 5. Place Order
        order_post = self.client.post(reverse('orders:checkout'), {
            'full_name': 'Sophia Montgomery',
            'email': 'sophia@example.com',
            'phone': '+91 9876543210',
            'street_address': '12 Palace Road',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'postal_code': '560001',
            'country': 'India',
            'payment_method': 'card',
            'order_notes': 'Please ensure antique brass eyelets.'
        })
        self.assertEqual(order_post.status_code, 302)
        
        # Verify order was saved
        order = Order.objects.filter(email='sophia@example.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.status, 'Confirmed')

        # 6. Order Success Page
        success_page = self.client.get(reverse('orders:order_success', kwargs={'order_number': order.order_number}))
        self.assertEqual(success_page.status_code, 200)
        self.assertContains(success_page, order.order_number)

        # 7. Order Invoice Page
        invoice_page = self.client.get(reverse('orders:order_invoice', kwargs={'order_number': order.order_number}))
        self.assertEqual(invoice_page.status_code, 200)
        self.assertContains(invoice_page, order.order_number)

        # 8. Order Tracking
        track_page = self.client.get(reverse('orders:track_order'), {'order_number': order.order_number})
        self.assertEqual(track_page.status_code, 200)
        self.assertContains(track_page, order.order_number)

    def test_product_review(self):
        self.client.force_login(self.customer)
        review_post = self.client.post(reverse('products:submit_review', kwargs={'slug': self.product.slug}), {
            'rating': 5,
            'title': 'Exquisite craftsmanship & drape weight',
            'comment': 'The velvet has a gorgeous sheen and blocks light flawlessly.'
        })
        self.assertEqual(review_post.status_code, 302)
        self.assertEqual(ProductReview.objects.filter(product=self.product).count(), 1)
