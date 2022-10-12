from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Category, Product, Profile, FavouriteProducts, Customer
from django.views.generic import ListView, DetailView
from .forms import LoginForm, RegistrationForm, UserCityForm, UserFirstNameForm, UserLastNameForm, UserPhoneForm, \
    ShippingForm, CustomerForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .utils import CartForAuthenticatedUser, get_cart_data
from mebel import settings
import stripe


# Create your views here.

class ProductList(ListView):
    model = Product
    extra_context = {
        'title': 'Aurora: Главная страница'
    }
    template_name = 'mebel_app/product_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        categories = Category.objects.all()
        data = []
        for category in categories:
            products = category.products.all()[:4]

            if category.image:
                image = category.image.url
            else:
                image = '-'
            data.append({
                'title': category,
                'products': products,
                'image': image

            })
        return data


class ProductListByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'mebel_app/category_detail.html'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = category.products.all()
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'Категория: {category.title}'
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'mebel_app/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'Товар - {product.title}'

        return context


class About(ListView):
    model = Product
    context_object_name = 'about'
    template_name = 'mebel_app/about.html'

    data = []
    data.append({
        'title': 'О нас'
    })


def login_registration(request):
    context = {
        'title': 'Войти или зарегестрироваться',
        'login_form': LoginForm(),
        'registration_form': RegistrationForm()
    }
    return render(request, 'mebel_app/login_registration.html', context)


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('product_list')
    else:
        messages.error(request, 'Не верное имя пользователя или пароль')
        return redirect('login_registration')


def user_logout(request):
    logout(request)
    return redirect('product_list')


def register(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        profile = Profile.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)

        messages.success(request, 'Аккаунт успешно создан. Войдите в аккаунт!')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error][0])
    return redirect('login_registration')


def save_or_delete_fav(request, product__slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=product__slug)
    if user:
        favs = FavouriteProducts.objects.filter(user=user)
        if product in [i.product for i in favs]:
            fav_product = FavouriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavouriteProducts.objects.create(user=user, product=product)
    next_page = request.META.get('HTTP_REFERER', 'product_list')
    return redirect(next_page)


class FavouriteProductsView(ListView):
    model = FavouriteProducts
    context_object_name = 'products'
    template_name = 'mebel_app/favorites.html'

    def get_queryset(self):
        user = self.request.user
        favs = FavouriteProducts.objects.filter(user=user)
        products = [i.product for i in favs]
        return products


def cart(request):
    cart_info = get_cart_data(request)
    context = {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'products': cart_info['order_products'],
        'title': 'Корзина',
        'cart_total_price': cart_info['cart_total_price']
    }
    return render(request, 'mebel_app/cart.html', context)
class SearchResults(ListView):
    model = Product
    template_name = 'mebel_app/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(title__icontains=word)
        return products


def to_cart(request, product_id, action):
    user_cart = CartForAuthenticatedUser(request, product_id, action)
    product = Product.objects.get(pk=product_id)
    if action == 'first_add':
        messages.success(request, 'Товар успешно добавлен в корзину!')
        return redirect('detail_product_list', product.slug)
    elif action == 'delete' or 'add':
        return redirect('cart')


def delete_all_quantity(request, pk):
    user_cart = CartForAuthenticatedUser(request, pk).delete_all_quantity(pk)
    next_page = request.META.get('HTTP_REFERER', 'cart')
    return redirect(next_page)


def clear_cart(request):
    user_cart = CartForAuthenticatedUser(request).clear_all_cart()
    return redirect('cart')


def checkout(request):
    cart_info = get_cart_data(request)
    context = {
        'customer_form': CustomerForm(),
        'shipping_form': ShippingForm(),
        'title': 'Оформление заказа',
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'products': cart_info['order_products'],
        'profile': Profile.objects.get(user=request.user)
    }
    return render(request, 'mebel_app/checkout.html', context)


def user_page(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'title': 'Личный кабинет',
        'profile': profile
    }
    return render(request, 'mebel_app/profile.html', context)





def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        customer_form = CustomerForm(data=request.POST)
        print(customer_form)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data['first_name']
            customer.last_name = customer_form.cleaned_data['last_name']
            customer.email = customer_form.cleaned_data['email']
            customer.phone_number = customer_form.cleaned_data['phone_number']
            customer.save()
            customer_form.save()
        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.order = user_cart.get_cart_info()['order']
            address.customer = Customer.objects.get(user=request.user)
            address.save()
        total_price = cart_info['cart_total_price']
        total_quantity = cart_info['cart_total_quantity']
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Товары LoftMebel'
                    },
                    'unit_amount': int(((total_price / total_quantity) / 10320) * 100)
                },
                'quantity': total_quantity
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('success'))
        )
        return redirect(session.url, 303)


def successPayment(request):
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear()
    return render(request, 'mebel_app/success.html')


def name_form(request):
    if request.method == 'POST':
        form = UserFirstNameForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно изменено!')
            return redirect('profile')
    else:
        form = UserFirstNameForm(instance=request.user)
        context = {
            'title': 'Изменить Имя',
            'form': form
        }
        return render(request, 'mebel_app/name_form.html', context)


def last_name_form(request):
    if request.method == 'POST':
        form = UserLastNameForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно изменено!')
            return redirect('profile')
    else:
        form = UserLastNameForm(instance=request.user)
        context = {
            'title': 'Изменить Фамилию',
            'form': form
        }
        return render(request, 'mebel_app/last_name_form.html', context)


def phone_form(request, pk):
    if request.method == 'POST':
        profile = Profile.objects.get(pk=pk)
        form = UserPhoneForm(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно изменено!')
            return redirect('profile')
    else:
        profile = Profile.objects.get(pk=pk)
        form = UserPhoneForm(instance=profile)
        context = {
            'title': 'Изменение номера телефона',
            'form': form
        }
        return render(request, 'mebel_app/phone_form.html', context)


def city_form(request, pk):
    if request.method == 'POST':
        profile = Profile.objects.get(pk=pk)
        form = UserCityForm(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно изменено!')
            return redirect('profile')
    else:
        profile = Profile.objects.get(pk=pk)
        form = UserCityForm(instance=profile)
        context = {
            'title': 'Изменение города',
            'form': form
        }
        return render(request, 'mebel_app/city_form.html', context)
