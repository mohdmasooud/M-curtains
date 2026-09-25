from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.user_app.models import Product, Category, Fabric, Order, OrderItem, Coupon

class AdminAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Staff Admin User
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@mcurtains.com',
            password='AdminPassword2026!',
            is_staff=True,
            is_superuser=True
        )
        
        # Regular Customer (Non-staff)
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='customer@example.com',
            password='CustomerPassword123!',
            is_staff=False
        )
        
        # Initial Category & Product & Order for testing
        self.category = Category.objects.create(
            name='Jacquard Weave',
            slug='jacquard-weave',
            description='Intricate woven damask patterns'
        )
        
        self.fabric = Fabric.objects.create(
            name='Belgian Jacquard Linen',
            slug='belgian-jacquard',
            composition='70% Linen, 30% Cotton'
        )
        
        self.product = Product.objects.create(
            name='Versailles Damask Jacquard Curtain',
            slug='versailles-damask-jacquard-curtain',
            category=self.category,
            fabric=self.fabric,
            short_description='Opulent baroque woven damask',
            description='Detailed Jacquard weave.',
            base_price=Decimal('3499.00'),
            stock_quantity=25,
            blackout_percentage=75,
            is_available=True
        )
        
        self.order = Order.objects.create(
            user=self.regular_user,
            full_name='Arthur Pendelton',
            email='arthur@example.com',
            phone='+91 9988776655',
            street_address='10 Kensington Mansions',
            city='Delhi',
            state='Delhi',
            postal_code='110001',
            country='India',
            subtotal=Decimal('3499.00'),
            total_amount=Decimal('3499.00'),
            status='Pending'
        )
        
        self.coupon = Coupon.objects.create(
            code='SAVE10',
            discount_percentage=10,
            min_purchase_amount=Decimal('500.00'),
            is_active=True
        )

    def test_admin_access_control(self):
        # 1. Anonymous user accessing dashboard -> redirected to login
        response = self.client.get(reverse('store_admin:dashboard'))
        self.assertEqual(response.status_code, 302)
        
        # 2. Non-staff user logged in accessing dashboard -> redirected
        self.client.force_login(self.regular_user)
        response = self.client.get(reverse('store_admin:dashboard'))
        self.assertEqual(response.status_code, 302)
        
        # 3. Staff user logged in -> 200 OK
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('store_admin:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'Management Portal')

    def test_admin_login_view(self):
        login_page = self.client.get(reverse('store_admin:login'))
        self.assertEqual(login_page.status_code, 200)

        # Non-staff login attempt
        fail_res = self.client.post(reverse('store_admin:login'), {
            'username': 'regularuser',
            'password': 'CustomerPassword123!'
        })
        self.assertEqual(fail_res.status_code, 200)
        self.assertContains(fail_res, 'Access denied')

        # Staff login attempt
        success_res = self.client.post(reverse('store_admin:login'), {
            'username': 'adminuser',
            'password': 'AdminPassword2026!'
        })
        self.assertEqual(success_res.status_code, 302)

    def test_products_management_crud(self):
        self.client.force_login(self.admin_user)
        
        # 1. Product List
        list_res = self.client.get(reverse('store_admin:products_list'))
        self.assertEqual(list_res.status_code, 200)
        self.assertContains(list_res, self.product.name)

        # 2. Add Product GET and POST
        add_get = self.client.get(reverse('store_admin:product_add'))
        self.assertEqual(add_get.status_code, 200)
        
        add_post = self.client.post(reverse('store_admin:product_add'), {
            'name': 'Nordic Frost Sheer Drapery',
            'category': self.category.id,
            'fabric': self.fabric.id,
            'short_description': 'Ethereal sheer curtain',
            'description': 'Diffusion of daylight.',
            'base_price': '1899.00',
            'stock_quantity': 30,
            'blackout_percentage': 20,
            'default_width_cm': 140,
            'default_drop_cm': 225,
            'color_name': 'Frost White',
            'color_hex': '#F0F8FF',
            'is_available': True
        })
        self.assertEqual(add_post.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Nordic Frost Sheer Drapery').exists())
        
        new_prod = Product.objects.get(name='Nordic Frost Sheer Drapery')

        # 3. Edit Product
        edit_post = self.client.post(reverse('store_admin:product_edit', kwargs={'pk': new_prod.pk}), {
            'name': 'Nordic Frost Sheer Drapery (Updated)',
            'category': self.category.id,
            'fabric': self.fabric.id,
            'short_description': 'Ethereal sheer curtain updated',
            'description': 'Diffusion of daylight.',
            'base_price': '1999.00',
            'stock_quantity': 35,
            'blackout_percentage': 20,
            'default_width_cm': 140,
            'default_drop_cm': 225,
            'color_name': 'Frost White',
            'color_hex': '#F0F8FF',
            'is_available': True
        })
        self.assertEqual(edit_post.status_code, 302)
        new_prod.refresh_from_db()
        self.assertEqual(new_prod.name, 'Nordic Frost Sheer Drapery (Updated)')

        # 4. Delete Product
        del_post = self.client.post(reverse('store_admin:product_delete', kwargs={'pk': new_prod.pk}))
        self.assertEqual(del_post.status_code, 302)
        self.assertFalse(Product.objects.filter(name='Nordic Frost Sheer Drapery (Updated)').exists())

    def test_categories_management_crud(self):
        self.client.force_login(self.admin_user)
        
        # 1. Categories List
        list_res = self.client.get(reverse('store_admin:categories_list'))
        self.assertEqual(list_res.status_code, 200)

        # 2. Add Category
        add_res = self.client.post(reverse('store_admin:category_add'), {
            'name': 'Pure Silk Voile',
            'slug': 'pure-silk-voile',
            'description': 'Handcrafted pure mulberry silk voile'
        })
        self.assertEqual(add_res.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Pure Silk Voile').exists())
        
        cat = Category.objects.get(name='Pure Silk Voile')

        # 3. Edit Category
        edit_res = self.client.post(reverse('store_admin:category_edit', kwargs={'pk': cat.pk}), {
            'name': 'Pure Silk Voile Atelier',
            'slug': 'pure-silk-voile-atelier',
            'description': 'Updated description'
        })
        self.assertEqual(edit_res.status_code, 302)
        cat.refresh_from_db()
        self.assertEqual(cat.name, 'Pure Silk Voile Atelier')

        # 4. Delete Category
        del_res = self.client.post(reverse('store_admin:category_delete', kwargs={'pk': cat.pk}))
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(Category.objects.filter(name='Pure Silk Voile Atelier').exists())

    def test_orders_management(self):
        self.client.force_login(self.admin_user)
        
        # 1. Orders List
        list_res = self.client.get(reverse('store_admin:orders_list'))
        self.assertEqual(list_res.status_code, 200)
        self.assertContains(list_res, self.order.order_number)

        # 2. Order Detail
        detail_res = self.client.get(reverse('store_admin:order_detail', kwargs={'order_number': self.order.order_number}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, self.order.order_number)

        # 3. Update Order Status
        update_res = self.client.post(reverse('store_admin:order_update_status', kwargs={'order_number': self.order.order_number}), {
            'status': 'Tailoring',
            'payment_status': 'Paid',
            'tracking_number': 'FEDEX-ATELIER-892',
            'admin_notes': 'Fabric cut and sent for hand pleating.'
        })
        self.assertEqual(update_res.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Tailoring')
        self.assertEqual(self.order.tracking_number, 'FEDEX-ATELIER-892')

    def test_customers_management(self):
        self.client.force_login(self.admin_user)
        
        # 1. Customer List
        list_res = self.client.get(reverse('store_admin:customers_list'))
        self.assertEqual(list_res.status_code, 200)
        self.assertContains(list_res, self.regular_user.username)

        # 2. Toggle Status
        toggle_res = self.client.get(reverse('store_admin:customer_toggle_status', kwargs={'user_id': self.regular_user.id}))
        self.assertEqual(toggle_res.status_code, 302)
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_active)

    def test_coupons_management(self):
        self.client.force_login(self.admin_user)
        
        # 1. Coupon List
        list_res = self.client.get(reverse('store_admin:coupons_list'))
        self.assertEqual(list_res.status_code, 200)
        self.assertContains(list_res, 'SAVE10')

        # 2. Add Coupon
        add_res = self.client.post(reverse('store_admin:coupon_add'), {
            'code': 'SUMMER30',
            'discount_percentage': 30,
            'min_purchase_amount': '1500.00',
            'is_active': True
        })
        self.assertEqual(add_res.status_code, 302)
        self.assertTrue(Coupon.objects.filter(code='SUMMER30').exists())

        # 3. Toggle Coupon
        coupon = Coupon.objects.get(code='SUMMER30')
        toggle_res = self.client.get(reverse('store_admin:coupon_toggle', kwargs={'pk': coupon.pk}))
        self.assertEqual(toggle_res.status_code, 302)
        coupon.refresh_from_db()
        self.assertFalse(coupon.is_active)

        # 4. Delete Coupon
        del_res = self.client.post(reverse('store_admin:coupon_delete', kwargs={'pk': coupon.pk}))
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(Coupon.objects.filter(code='SUMMER30').exists())

    def test_direct_sql_console(self):
        self.client.force_login(self.admin_user)
        
        # 1. SQL Console GET
        console_get = self.client.get(reverse('store_admin:sql_console'))
        self.assertEqual(console_get.status_code, 200)
        self.assertContains(console_get, 'SQL Console')

        # 2. SQL SELECT Query POST
        sql_post = self.client.post(reverse('store_admin:sql_console'), {
            'sql_query': 'SELECT name, base_price, stock_quantity FROM user_app_product;'
        })
        self.assertEqual(sql_post.status_code, 200)
        self.assertContains(sql_post, self.product.name)

        # 3. SQL Invalid Query POST (Verify robust error handling)
        sql_err_post = self.client.post(reverse('store_admin:sql_console'), {
            'sql_query': 'SELECT * FROM nonexistent_drapery_table;'
        })
        self.assertEqual(sql_err_post.status_code, 200)
        self.assertContains(sql_err_post, 'no such table')
