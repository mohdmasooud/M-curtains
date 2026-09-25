from .models import Category
from .cart import Cart

def categories_processor(request):
    """Provides navigation categories for header mega menu."""
    return {
        'nav_categories': Category.objects.all()[:8],
    }

def cart_processor(request):
    """Provides live cart object and total items count to all templates."""
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_total_items': len(cart),
    }
