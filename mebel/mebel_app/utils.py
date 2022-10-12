from .models import Product, Order, OrderProduct, Customer


class CartForAuthenticatedUser:
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user
        if product_id and action:
            self.add_or_delete(product_id, action)

    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(user=self.user, first_name=self.user.first_name,
                                                           last_name=self.user.last_name, email=self.user.email)
        order, created = Order.objects.get_or_create(customer=customer)
        order_products = order.orderproduct_set.all()
        cart_total_quantity = order.get_cart_total_quantity
        cart_total_price = order.get_cart_total_price

        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'order': order,
            'order_products': order_products
        }

    def add_or_delete(self, product_id, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(pk=product_id)
        print(product)
        order_product, created = OrderProduct.objects.get_or_create(order=order,
                                                                    product=product)
        if action == 'add' and product.quantity > 0:
            order_product.quantity += 1  # +1 в корзине
            product.quantity -= 1  # -1 Со склада
        else:
            order_product.quantity -= 1
            product.quantity += 1
        order_product.save()
        product.save()

    def clear(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for product in order_products:
            product.delete()
        order.save()

    def delete_all_quantity(self, pk):
        order = self.get_cart_info()['order']
        product = Product.objects.get(pk=pk)
        order_product = OrderProduct.objects.get(order=order, product=product)
        product.quantity += order_product.quantity
        order_product.delete()
        product.save()
        order.save()

    def clear_all_cart(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for item in order_products:
            item_product_pk = item.product.pk
            product = Product.objects.get(pk=item_product_pk)
            product.quantity += item.quantity
            item.delete()
            product.save()
        order.save()


def get_cart_data(request):
    user_cart = CartForAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()

    return {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'cart_total_price': cart_info['cart_total_price'],
        'order': cart_info['order'],
        'order_products': cart_info['order_products']
    }
