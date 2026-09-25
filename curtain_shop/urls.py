from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Standard Django Admin
    path('django-admin/', admin.site.urls),
    
    # 2. Admin Application (Custom Admin Portal & Management)
    path('store-admin/', include(('apps.admin_app.urls', 'admin_app'), namespace='admin_app')),
    path('store-admin/', include(('apps.admin_app.urls', 'store_admin'), namespace='store_admin')),
    
    # 1. User Application (Storefront, Auth, Catalog, Cart, Orders)
    path('', include(('apps.user_app.urls', 'user_app'), namespace='user_app')),
    # Route aliases for legacy template compatibility
    path('', include(('apps.user_app.urls', 'core'), namespace='core')),
    path('', include(('apps.user_app.urls', 'accounts'), namespace='accounts')),
    path('', include(('apps.user_app.urls', 'products'), namespace='products')),
    path('', include(('apps.user_app.urls', 'cart'), namespace='cart')),
    path('', include(('apps.user_app.urls', 'orders'), namespace='orders')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
