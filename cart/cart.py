from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):  # class to manage shopping cart

    def __init__(self, request):
        """ initialize the cart with request object"""
        self.session = request.session  # to make it accessible	to	the	other methods of the Cart class.
        # add products to cart by product id
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # product to add/update in cart, default quan=1
    def add(self, product, quantity=1, update_quantity=False):
        """ Add a product to the cart or update its quantity ."""
        product_id = str(
            product.id)  # as key in cart contents's dictionary, in str coz django uses json to serialize session data
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(
                product.price)}  # price in str to serialize it
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as 'modified' to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """" remove a product from the cart"""
        product_id = str(product.id)  # json format takes string only
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

     # method iterate	through	the	items contained	in the cart and access	the	related	Product	instances.
    def __iter__(self):
        """ Iterate	over the items in the cart and get the
            products from the	database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']  # total price attribute
            yield item

    def __len__(self):
        """ count all items in the cart """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """ total price of  items in the cart """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
