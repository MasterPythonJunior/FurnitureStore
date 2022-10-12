from .views import *
from django.urls import path

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('category/<slug:slug>/', ProductListByCategory.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product'),
    path('login_registration/', login_registration, name='login_registration'),
    path('about', About.as_view(), name='about'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('add-or-delete/<slug:product__slug>/', save_or_delete_fav, name='save_or_del'),
    path('favourite/', FavouriteProductsView.as_view(), name='favourite'),
    path('cart/', cart, name='cart'),
    path('change_name/', name_form, name='name_form'),
    path('change_last_name/', last_name_form, name='last_name_form'),
    path('change_phone/<int:pk>', phone_form, name='phone_form'),
    path('change_city/<int:pk>', city_form, name='city_form'),
    path('search/', SearchResults.as_view(), name='search'),

    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('delete_all_quantity/<int:pk>', delete_all_quantity, name='delete_all_quantity'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('checkout/', checkout, name='checkout'),
    path('profile/', user_page, name='profile'),
    path('payment', create_checkout_session, name='payment'),
    path('success_payment/', successPayment, name='success')

]
