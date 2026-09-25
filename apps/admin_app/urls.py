from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    # Custom Admin Authentication
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'),
    
    # Custom Admin Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Direct SQL Database Console
    path('sql-console/', views.sql_console_view, name='sql_console'),
    
    # Products Management
    path('products/', views.products_list_view, name='products_list'),
    path('products/add/', views.product_add_view, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete_view, name='product_delete'),
    
    # Categories Management
    path('categories/', views.categories_list_view, name='categories_list'),
    path('categories/add/', views.category_add_view, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit_view, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete_view, name='category_delete'),
    
    # Orders Management
    path('orders/', views.orders_list_view, name='orders_list'),
    path('orders/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('orders/<str:order_number>/update-status/', views.order_update_status_view, name='order_update_status'),
    
    # Customers Management
    path('customers/', views.customers_list_view, name='customers_list'),
    path('customers/<int:user_id>/toggle-status/', views.customer_toggle_status_view, name='customer_toggle_status'),
    
    # Coupons Management
    path('coupons/', views.coupons_list_view, name='coupons_list'),
    path('coupons/add/', views.coupon_add_view, name='coupon_add'),
    path('coupons/<int:pk>/toggle/', views.coupon_toggle_view, name='coupon_toggle'),
    path('coupons/<int:pk>/delete/', views.coupon_delete_view, name='coupon_delete'),
]
