from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('store/', views.home, name='home'),
    path('category/<str:category_name>/', views.category_view, name='category'),
    path('search/', views.search_view, name='search'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('interact/<int:product_id>/', views.interact_product, name='interact'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('info/<str:page_slug>/', views.info_view, name='info'),
]