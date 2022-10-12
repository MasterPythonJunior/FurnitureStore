from django.db import models

# Create your models here.
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория', unique=True)
    image = models.FileField(upload_to='categories/', verbose_name='Иконка')
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг')

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название товара', unique=True)
    color = models.CharField(max_length=50, verbose_name='Цвет')
    price = models.FloatField(max_length=20, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    description = models.TextField(verbose_name='Описание товара')
    quantity = models.IntegerField(verbose_name='Кол-во на складе')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.first().photo.url
            except:
                return 'D:\Мухаммад Азиз\Диплогм\Проект\assets\icons\LOGO.svg'
        else:
            return 'D:\Мухаммад Азиз\Диплогм\Проект\assets\icons\LOGO.svg'

    def get_photo(self):
        if self.images:
            try:
                return self.photo.url
            except:
                return 'D:\Мухаммад Азиз\Диплогм\Проект\assets\icons\LOGO.svg'
        else:
            return 'D:\Мухаммад Азиз\Диплогм\Проект\assets\icons\LOGO.svg'

    def get_height_size(self):
        if self.sizes:
            try:
                return self.sizes.first().height
            except:
                return '0'
        else:
            return '0'

    def get_width_size(self):
        if self.sizes:
            try:
                return self.sizes.first().width
            except:
                return '0'
        else:
            return '0'

    def get_depth_size(self):
        if self.sizes:
            try:
                return self.sizes.first().depth
            except:
                return '0'
        else:
            return '0'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Gallery(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to='product/', null=True, blank=True, verbose_name='Изображения')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'


class Size(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='sizes')
    height = models.IntegerField(verbose_name='Высота', null=False)
    width = models.IntegerField(verbose_name='Ширина', null=False)
    depth = models.IntegerField(verbose_name='Глубина', null=False)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Cities(models.Model):
    city = models.CharField(max_length=150, verbose_name='Город')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, verbose_name='Город', null=True, blank=True)
    phone_number = models.CharField(max_length=200, verbose_name='Номер телефона', blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class FavouriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return f'{self.user.username} - {self.product.title}'

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class Customer(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=150, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', null=True)
    email = models.EmailField(verbose_name='Почта', null=True)
    phone_number = models.CharField(max_length=250, verbose_name='Номер телефона', null=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан в')
    is_completed = models.BooleanField(default=False, verbose_name='Сделан ли')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return str(self.pk) + ' '

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        order_product = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_product])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_product = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_product])
        return total_quantity


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Товар')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add='True', verbose_name='Добавлен в')

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'

    @property
    def get_total_price(self):
        print('Объект продукта: ', self.product)
        print('Объект продукта: ', self.quantity)
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заказчик')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заказ')
    address = models.CharField(max_length=250, verbose_name='Адрес доставки')
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Во сколько создан адрес')

    def __str__(self):
        return str(f'{self.customer.first_name} {self.address}')

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'
