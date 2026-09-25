from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count, Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import connection
from apps.user_app.models import Product, Category, Fabric, ProductImage, Order, OrderItem, Coupon
from .decorators import staff_required
from .forms import ProductAdminForm, CategoryAdminForm, FabricAdminForm, OrderStatusUpdateForm, CouponAdminForm
from decimal import Decimal
import json
import time

# --- Custom Admin Authentication ---

def admin_login_view(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('store_admin:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f"Welcome back to M Curtains Atelier Management, {user.first_name or user.username}!")
                next_url = request.GET.get('next') or request.POST.get('next') or 'store_admin:dashboard'
                return redirect(next_url)
            else:
                messages.error(request, "Access denied. You do not have staff administrator privileges.")
        else:
            messages.error(request, "Invalid administrator username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'store_admin/login.html', {'form': form})


def admin_logout_view(request):
    logout(request)
    messages.info(request, "You have been securely signed out of the Management Portal.")
    return redirect('store_admin:login')


# --- Admin Dashboard ---

@staff_required
def dashboard_view(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(payment_status='Paid').aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    pending_orders = Order.objects.filter(status__in=['Pending', 'Confirmed', 'Tailoring']).count()
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock_quantity__lte=15).count()
    total_customers = User.objects.filter(is_staff=False).count()

    recent_orders = Order.objects.order_by('-created_at')[:8]
    low_stock_items = Product.objects.filter(stock_quantity__lte=15)[:6]
    top_products = Product.objects.filter(is_bestseller=True)[:6]

    # Chart data: Orders by status
    status_counts = Order.objects.values('status').annotate(count=Count('id'))
    status_labels = [s['status'] for s in status_counts]
    status_data = [s['count'] for s in status_counts]

    # Category product counts
    category_counts = Category.objects.annotate(prod_count=Count('products')).values('name', 'prod_count')
    category_labels = [c['name'] for c in category_counts]
    category_data = [c['prod_count'] for c in category_counts]

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_customers': total_customers,
        'recent_orders': recent_orders,
        'low_stock_items': low_stock_items,
        'top_products': top_products,
        'status_labels_json': json.dumps(status_labels),
        'status_data_json': json.dumps(status_data),
        'category_labels_json': json.dumps(category_labels),
        'category_data_json': json.dumps(category_data),
    }
    return render(request, 'store_admin/dashboard.html', context)


# --- Products Management ---

@staff_required
def products_list_view(request):
    products = Product.objects.select_related('category', 'fabric').all()
    
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    stock_filter = request.GET.get('stock', '')

    if q:
        products = products.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
    if category_id:
        products = products.filter(category_id=category_id)
    if stock_filter == 'low':
        products = products.filter(stock_quantity__lte=15)
    elif stock_filter == 'out':
        products = products.filter(stock_quantity=0)

    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    categories = Category.objects.all()

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'q': q,
        'selected_category': category_id,
        'selected_stock': stock_filter,
    }
    return render(request, 'store_admin/products_list.html', context)


@staff_required
def product_add_view(request):
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Curtain '{product.name}' added successfully!")
            return redirect('store_admin:products_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProductAdminForm()

    return render(request, 'store_admin/product_form.html', {'form': form, 'title': 'Add New Curtain Product'})


@staff_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect('store_admin:products_list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProductAdminForm(instance=product)

    return render(request, 'store_admin/product_form.html', {'form': form, 'title': f'Edit: {product.name}', 'product': product})


@staff_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' deleted.")
        return redirect('store_admin:products_list')
    return render(request, 'store_admin/product_confirm_delete.html', {'product': product})


# --- Categories Management ---

@staff_required
def categories_list_view(request):
    categories = Category.objects.annotate(prod_count=Count('products')).all()
    form = CategoryAdminForm()
    return render(request, 'store_admin/categories_list.html', {'categories': categories, 'form': form})


@staff_required
def category_add_view(request):
    if request.method == 'POST':
        form = CategoryAdminForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Category '{cat.name}' created.")
        else:
            messages.error(request, "Error creating category.")
    return redirect('store_admin:categories_list')


@staff_required
def category_edit_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryAdminForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated.")
            return redirect('store_admin:categories_list')
    else:
        form = CategoryAdminForm(instance=category)
    return render(request, 'store_admin/category_form.html', {'form': form, 'category': category})


@staff_required
def category_delete_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f"Category '{name}' deleted.")
        return redirect('store_admin:categories_list')
    return render(request, 'store_admin/category_confirm_delete.html', {'category': category})


# --- Orders Management ---

@staff_required
def orders_list_view(request):
    orders = Order.objects.prefetch_related('items').all()

    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    payment_status = request.GET.get('payment_status', '')

    if q:
        orders = orders.filter(Q(order_number__icontains=q) | Q(full_name__icontains=q) | Q(email__icontains=q))
    if status:
        orders = orders.filter(status=status)
    if payment_status:
        orders = orders.filter(payment_status=payment_status)

    paginator = Paginator(orders, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'orders': page_obj.object_list,
        'page_obj': page_obj,
        'status_choices': Order.STATUS_CHOICES,
        'q': q,
        'selected_status': status,
        'selected_payment_status': payment_status,
    }
    return render(request, 'store_admin/orders_list.html', context)


@staff_required
def order_detail_view(request, order_number):
    order = get_object_or_404(Order.objects.prefetch_related('items'), order_number=order_number)
    form = OrderStatusUpdateForm(instance=order)
    return render(request, 'store_admin/order_detail.html', {'order': order, 'form': form})


@staff_required
def order_update_status_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Order #{order.order_number} status updated to '{order.status}'!")
        else:
            messages.error(request, "Could not update order status.")
    return redirect('store_admin:order_detail', order_number=order_number)


# --- Customer Management ---

@staff_required
def customers_list_view(request):
    customers = User.objects.filter(is_staff=False).annotate(
        order_count=Count('orders'),
        total_spend=Sum('orders__total_amount')
    ).order_by('-date_joined')

    q = request.GET.get('q', '').strip()
    if q:
        customers = customers.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))

    paginator = Paginator(customers, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'store_admin/customers_list.html', {'customers': page_obj.object_list, 'page_obj': page_obj, 'q': q})


@staff_required
def customer_toggle_status_view(request, user_id):
    customer = get_object_or_404(User, id=user_id)
    customer.is_active = not customer.is_active
    customer.save()
    status_str = "activated" if customer.is_active else "deactivated"
    messages.success(request, f"Customer account '{customer.username}' has been {status_str}.")
    return redirect('store_admin:customers_list')


# --- Coupons Management ---

@staff_required
def coupons_list_view(request):
    coupons = Coupon.objects.all().order_by('-valid_from')
    form = CouponAdminForm()
    return render(request, 'store_admin/coupons_list.html', {'coupons': coupons, 'form': form})


@staff_required
def coupon_add_view(request):
    if request.method == 'POST':
        form = CouponAdminForm(request.POST)
        if form.is_valid():
            coupon = form.save(commit=False)
            coupon.code = coupon.code.upper()
            coupon.save()
            messages.success(request, f"Coupon '{coupon.code}' created!")
        else:
            messages.error(request, "Error creating coupon. Please check form values.")
    return redirect('store_admin:coupons_list')


@staff_required
def coupon_toggle_view(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    coupon.is_active = not coupon.is_active
    coupon.save()
    messages.success(request, f"Coupon '{coupon.code}' is now {'Active' if coupon.is_active else 'Inactive'}.")
    return redirect('store_admin:coupons_list')


@staff_required
def coupon_delete_view(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        code = coupon.code
        coupon.delete()
        messages.success(request, f"Coupon '{code}' deleted.")
    return redirect('store_admin:coupons_list')


# --- Direct SQL Execution Console Module ---

@staff_required
def sql_console_view(request):
    query_result = None
    columns = []
    rows = []
    error_message = None
    rows_affected = 0
    exec_time_ms = 0
    sql_query = request.POST.get('sql_query', '').strip() if request.method == 'POST' else ''

    # Get list of existing database tables for quick reference
    tables = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'django_%' AND name NOT LIKE 'auth_%' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
            tables = [row[0] for row in cursor.fetchall()]
    except Exception:
        tables = []

    if request.method == 'POST' and sql_query:
        start_time = time.time()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                exec_time_ms = round((time.time() - start_time) * 1000, 2)
                
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    rows_affected = len(rows)
                else:
                    rows_affected = cursor.rowcount
                    connection.commit()
        except Exception as e:
            error_message = str(e)
            exec_time_ms = round((time.time() - start_time) * 1000, 2)

    context = {
        'sql_query': sql_query,
        'columns': columns,
        'rows': rows,
        'error_message': error_message,
        'rows_affected': rows_affected,
        'exec_time_ms': exec_time_ms,
        'tables': tables,
    }
    return render(request, 'store_admin/sql_console.html', context)
