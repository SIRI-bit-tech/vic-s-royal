from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('search/', views.product_search, name='product_search'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    path('wishlist/count/', views.wishlist_count, name='wishlist_count'),
    path('send-support-message/', views.send_support_message, name='send_support_message'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]

