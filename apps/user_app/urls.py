from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
    # 1. Core & Storefront
    path('', views.home_view, name='home'),
    path('room-visualizer/', views.room_visualizer_view, name='room_visualizer'),
    path('measurement-guide/', views.measurement_guide_view, name='measurement_guide'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

    # 2. User Authentication & Profile
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/dashboard/', views.dashboard_view, name='dashboard'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/addresses/', views.address_list_view, name='address_list'),
    path('accounts/addresses/add/', views.address_add_view, name='address_add'),
    path('accounts/addresses/<int:address_id>/edit/', views.address_edit_view, name='address_edit'),
    path('accounts/addresses/<int:address_id>/delete/', views.address_delete_view, name='address_delete'),
    path('accounts/addresses/<int:address_id>/default/', views.address_set_default_view, name='address_set_default'),

    # 3. Products & Catalog
    path('products/', views.product_list_view, name='product_list'),
    path('products/category/<slug:slug>/', views.category_products_view, name='category_detail'),
    path('products/search-api/', views.search_api, name='search_api'),
    path('products/calculate-price/<int:product_id>/', views.calculate_price_api, name='calculate_price_api'),
    path('products/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('products/<slug:slug>/review/', views.submit_review_view, name='submit_review'),

    # 4. Shopping Bag & Cart
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add_view, name='cart_add'),
    path('cart/update/<str:item_key>/', views.cart_update_view, name='cart_update'),
    path('cart/remove/<str:item_key>/', views.cart_remove_view, name='cart_remove'),
    path('cart/clear/', views.cart_clear_view, name='cart_clear'),
    path('cart/coupon/apply/', views.coupon_apply_view, name='coupon_apply'),
    path('cart/coupon/apply-alias/', views.coupon_apply_view, name='apply_coupon'),
    path('cart/coupon/remove/', views.coupon_remove_view, name='coupon_remove'),
    path('cart/coupon/remove-alias/', views.coupon_remove_view, name='remove_coupon'),

    # 5. Orders & Checkout
    path('orders/checkout/', views.checkout_view, name='checkout'),
    path('orders/success/<str:order_number>/', views.order_success_view, name='order_success'),
    path('orders/history/', views.order_history_view, name='order_history'),
    path('orders/track/', views.track_order_view, name='track_order'),
    path('orders/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('orders/<str:order_number>/invoice/', views.order_invoice_view, name='order_invoice'),
]
