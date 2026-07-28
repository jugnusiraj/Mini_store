from django.urls import path
from . import views


urlpatterns = [

    path('', views.home,name='home'),

    path('register/', views.register,name='register'),

    path('login/', views.login_view,name='login'),

    path('logout/', views.logout_view,name="logout"),

    path("cart/", views.cart, name="cart"),

    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),

    path( "remove/<int:cart_id>/",views.remove_from_cart,name="remove_from_cart"),

    path( "update/<int:cart_id>/",views.update_quantity,name="update_quantity"),

    path("checkout/", views.checkout, name="checkout"),

    path("success/", views.success, name="success"),

    path("cancel/", views.cancel, name="cancel"),

    path("product/<int:id>/", views.product_detail, name="product_detail"),

    path('wishlist/', views.wishlist, name='wishlist'),

    path('add-to-wishlist/<int:product_id>/',views.add_to_wishlist,name='add_to_wishlist'),

    path("orders/", views.order_history, name="order_history"),
  
]

