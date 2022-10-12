from django import template
from mebel_app.models import Category, FavouriteProducts

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories


@register.simple_tag()
def get_favourite_products(user):
    favs = FavouriteProducts.objects.filter(user=user)
    products = [i.product for i in favs]
    return products


@register.simple_tag()
def get_range(product):
    data = []
    if product.quantity < 5:
        for i in range(1, product.quantity + 1):
            data.append(i)
    else:
        for i in range(1, 6):
            data.append(i)
    return data
