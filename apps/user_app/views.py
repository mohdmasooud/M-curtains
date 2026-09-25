from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from decimal import Decimal

from .models import (
    Product, Category, Fabric, RoomType, PleatType, LiningType, 
    ProductReview, Coupon, Order, OrderItem, UserProfile, ShippingAddress
)
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm, 
    ShippingAddressForm, ProductReviewForm
)
from .cart import Cart


# ==========================================================================
# 1. CORE & BRANDING VIEWS
# ==========================================================================

def home_view(request):
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:6]
    bestsellers = Product.objects.filter(is_bestseller=True, is_available=True)
    if not bestsellers.exists():
        bestsellers = Product.objects.filter(is_available=True)[:4]
    else:
        bestsellers = bestsellers[:4]
        
    new_arrivals = Product.objects.filter(is_new_arrival=True, is_available=True)[:4]
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'new_arrivals': new_arrivals,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)


def room_visualizer_view(request):
    categories = Category.objects.all()
    fabrics = Fabric.objects.all()
    products = Product.objects.filter(is_available=True)[:8]
    context = {
        'categories': categories,
        'fabrics': fabrics,
        'products': products,
    }
    return render(request, 'core/room_visualizer.html', context)


def measurement_guide_view(request):
    pleats = PleatType.objects.all()
    linings = LiningType.objects.all()
    context = {
        'pleats': pleats,
        'linings': linings,
    }
    return render(request, 'core/measurement_guide.html', context)


def about_view(request):
    return render(request, 'core/about.html')


def contact_view(request):
    if request.method == 'POST':
        messages.success(request, "Thank you for contacting M Curtains Artisans. Our design concierge will contact you within 24 hours.")
        return redirect('user_app:contact')
    return render(request, 'core/contact.html')


# ==========================================================================
# 2. USER AUTHENTICATION & PROFILE VIEWS
# ==========================================================================

def register_view(request):
    if request.user.is_authenticated:
        return redirect('user_app:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"Welcome to M Curtains Atelier, {user.first_name or user.username}! Your account has been created.")
            login(request, user)
            return redirect('user_app:dashboard')
        else:
            messages.error(request, "Please correct the highlighted errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_app:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next') or request.POST.get('next') or 'user_app:dashboard'
                if user.is_staff and not request.GET.get('next'):
                    return redirect('store_admin:dashboard')
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('user_app:home')


@login_required
def dashboard_view(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    recent_orders = orders[:5]
    total_orders = orders.count()
    addresses = ShippingAddress.objects.filter(user=user)

    context = {
        'user': user,
        'recent_orders': recent_orders,
        'total_orders': total_orders,
        'addresses': addresses,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
        if form.is_valid():
            profile = form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('user_app:profile')
        else:
            messages.error(request, "Please correct the errors in the profile form.")
    else:
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


@login_required
def address_list_view(request):
    addresses = ShippingAddress.objects.filter(user=request.user)
    return render(request, 'accounts/address_list.html', {'addresses': addresses})


@login_required
def address_add_view(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if not ShippingAddress.objects.filter(user=request.user).exists():
                address.is_default = True
            address.save()
            messages.success(request, "Shipping address added successfully!")
            return redirect('user_app:address_list')
    else:
        form = ShippingAddressForm()
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add New Address'})


@login_required
def address_edit_view(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully!")
            return redirect('user_app:address_list')
    else:
        form = ShippingAddressForm(instance=address)
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Edit Address', 'address': address})


@login_required
def address_delete_view(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, "Address deleted.")
        return redirect('user_app:address_list')
    return render(request, 'accounts/address_confirm_delete.html', {'address': address})


@login_required
def address_set_default_view(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    ShippingAddress.objects.filter(user=request.user).update(is_default=False)
    address.is_default = True
    address.save()
    messages.success(request, f"{address.recipient_name}'s address is now set as default.")
    return redirect('user_app:address_list')


# ==========================================================================
# 3. PRODUCTS & CATALOG VIEWS
# ==========================================================================

def product_list_view(request):
    products = Product.objects.filter(is_available=True)

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) | 
            Q(description__icontains=q) | 
            Q(color_name__icontains=q) |
            Q(category__name__icontains=q)
        )

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Fabric filter
    fabric_slug = request.GET.get('fabric')
    if fabric_slug:
        products = products.filter(fabric__slug=fabric_slug)

    # Room filter
    room_slug = request.GET.get('room')
    if room_slug:
        products = products.filter(rooms__slug=room_slug)

    # Blackout filter
    blackout = request.GET.get('blackout')
    if blackout == 'blackout':
        products = products.filter(blackout_percentage__gte=95)
    elif blackout == 'sheer':
        products = products.filter(blackout_percentage__lte=30)
    elif blackout == 'room_darkening':
        products = products.filter(blackout_percentage__gte=50, blackout_percentage__lt=95)

    # Price range filter (in ₹)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(base_price__gte=Decimal(min_price))
        except Exception:
            pass
    if max_price:
        try:
            products = products.filter(base_price__lte=Decimal(max_price))
        except Exception:
            pass

    # Sorting
    sort_by = request.GET.get('sort', 'featured')
    if sort_by == 'price_low':
        products = products.order_by('base_price')
    elif sort_by == 'price_high':
        products = products.order_by('-base_price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'bestselling':
        products = products.filter(is_bestseller=True)

    # Pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'fabrics': Fabric.objects.all(),
        'rooms': RoomType.objects.all(),
        'selected_category': category_slug,
        'selected_fabric': fabric_slug,
        'selected_room': room_slug,
        'selected_blackout': blackout,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'q': q,
        'total_count': products.count(),
    }
    return render(request, 'products/product_list.html', context)


def category_products_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True)
    
    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'category': category,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
    }
    return render(request, 'products/category_products.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related('gallery_images', 'reviews__user'), slug=slug)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    
    pleats = PleatType.objects.all()
    linings = LiningType.objects.all()
    review_form = ProductReviewForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'pleats': pleats,
        'linings': linings,
        'review_form': review_form,
    }
    return render(request, 'products/product_detail.html', context)


def calculate_price_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        width = Decimal(request.GET.get('width', str(product.default_width_cm)))
        drop = Decimal(request.GET.get('drop', str(product.default_drop_cm)))
        pleat_id = request.GET.get('pleat_id')
        lining_id = request.GET.get('lining_id')

        pleat = PleatType.objects.filter(id=pleat_id).first() if pleat_id else None
        lining = LiningType.objects.filter(id=lining_id).first() if lining_id else None

        price = product.calculate_custom_price(width_cm=width, drop_cm=drop, pleat=pleat, lining=lining)
        return JsonResponse({
            'success': True,
            'calculated_price': float(price),
            'formatted_price': f"₹{price:,.2f}",
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def search_api(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(name__icontains=query) | Q(category__name__icontains=query) | Q(color_name__icontains=query)
    )[:6]

    results = []
    for p in products:
        results.append({
            'name': p.name,
            'slug': p.slug,
            'price': str(p.current_price),
            'image': p.display_image,
            'category': p.category.name,
        })

    return JsonResponse({'results': results})


@login_required
def submit_review_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your craftsmanship review has been submitted!")
        else:
            messages.error(request, "Error submitting review. Please check all fields.")
    return redirect('user_app:product_detail', slug=slug)


# ==========================================================================
# 4. CART & SHOPPING BAG VIEWS
# ==========================================================================

def cart_detail_view(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        width_cm = request.POST.get('width_cm')
        drop_cm = request.POST.get('drop_cm')
        pleat_id = request.POST.get('pleat_type')
        lining_id = request.POST.get('lining_type')

        cart.add(
            product=product,
            quantity=quantity,
            width_cm=width_cm,
            drop_cm=drop_cm,
            pleat_id=pleat_id,
            lining_id=lining_id
        )
        messages.success(request, f"Added {quantity}x '{product.name}' to your shopping bag.")
        return redirect('user_app:cart_detail')

    return redirect('user_app:product_detail', slug=product.slug)


def cart_update_view(request, item_key):
    if request.method == 'POST':
        cart = Cart(request)
        quantity = int(request.POST.get('quantity', 1))
        cart.update_quantity(item_key, quantity)
        messages.success(request, "Shopping bag updated.")
    return redirect('user_app:cart_detail')


def cart_remove_view(request, item_key):
    if request.method == 'POST' or request.method == 'GET':
        cart = Cart(request)
        cart.remove(item_key)
        messages.info(request, "Item removed from shopping bag.")
    return redirect('user_app:cart_detail')


def cart_clear_view(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Shopping bag cleared.")
    return redirect('user_app:cart_detail')


def coupon_apply_view(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip()
        cart = Cart(request)
        success, message = cart.apply_coupon(code)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    return redirect('user_app:cart_detail')


def coupon_remove_view(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart.remove_coupon()
        messages.info(request, "Promotional coupon removed.")
    return redirect('user_app:cart_detail')


# ==========================================================================
# 5. ORDERS & CHECKOUT VIEWS
# ==========================================================================

def checkout_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your shopping bag is empty.")
        return redirect('user_app:product_list')

    default_address = None
    if request.user.is_authenticated:
        default_address = ShippingAddress.objects.filter(user=request.user, is_default=True).first()
        if not default_address:
            default_address = ShippingAddress.objects.filter(user=request.user).first()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street_address = request.POST.get('street_address')
        apartment_suite = request.POST.get('apartment_suite', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country', 'India')
        payment_method = request.POST.get('payment_method', 'card')
        order_notes = request.POST.get('order_notes', '')

        order = Order(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            street_address=street_address,
            apartment_suite=apartment_suite,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            order_notes=order_notes,
            payment_method=payment_method,
            subtotal=cart.get_subtotal(),
            discount_amount=cart.get_discount_amount(),
            shipping_fee=cart.get_shipping_fee(),
            tax_amount=cart.get_tax_amount(),
            total_amount=cart.get_grand_total(),
            status='Confirmed',
            payment_status='Paid' if payment_method in ['card', 'upi'] else 'Pending',
        )
        order.save()

        # Create Order Items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                product_image_url=item['product'].display_image,
                unit_price=item['unit_price'],
                quantity=item['quantity'],
                total_price=item['total_price'],
                width_cm=item['width_cm'],
                drop_cm=item['drop_cm'],
                pleat_name=item['pleat_name'],
                lining_name=item['lining_name'],
            )

        # Clear cart
        cart.clear()
        messages.success(request, f"Order #{order.order_number} confirmed! Our master weavers have begun preparation.")
        return redirect('user_app:order_success', order_number=order.order_number)

    context = {
        'cart': cart,
        'default_address': default_address,
    }
    return render(request, 'orders/checkout.html', context)


def order_success_view(request, order_number):
    order = get_object_or_404(Order.objects.prefetch_related('items'), order_number=order_number)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


def order_detail_view(request, order_number):
    order = get_object_or_404(Order.objects.prefetch_related('items'), order_number=order_number)
    if request.user.is_authenticated and order.user and order.user != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('user_app:order_history')
    return render(request, 'orders/order_detail.html', {'order': order})


def order_invoice_view(request, order_number):
    order = get_object_or_404(Order.objects.prefetch_related('items'), order_number=order_number)
    return render(request, 'orders/invoice.html', {'order': order})


def track_order_view(request):
    order = None
    query = request.GET.get('order_number', '').strip()
    if query:
        order = Order.objects.filter(Q(order_number__iexact=query) | Q(tracking_number__iexact=query)).first()
        if not order:
            messages.warning(request, f"No order found matching identifier '{query}'.")

    return render(request, 'orders/track_order.html', {'order': order, 'query': query})
