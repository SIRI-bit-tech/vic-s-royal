from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from products.views import home, faq, customer_support, about
from dashboard.views import admin_dashboard
from products.sitemaps import ProductSitemap, CategorySitemap, StaticViewSitemap
from django.views.generic import TemplateView

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('products/', include('products.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('faq/', faq, name='faq'),
    path('customer-support/', customer_support, name='customer_support'),
    path('about/', about, name='about'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

