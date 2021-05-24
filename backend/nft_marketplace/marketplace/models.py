from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User as User_dj

from functools import reduce
# Create your models here.


class User(models.Model):
    pseudo = models.CharField(max_length=32)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    email = models.CharField(max_length=64)
    user_dj = models.ForeignKey(User_dj, on_delete=models.CASCADE)

    creation_date = models.DateTimeField('user creation date', auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} aka {self.pseudo}'

    def add_to_cart(self, uid):
        product = Product.objects.get(id=uid)
        cart, created = Cart.objects.get_or_create(user__id=self.pk)
        if not product or not product.selling or product.cart is not None:
            return False
        product.cart = cart
        product.selling = False
        cart.total_price += product.price
        cart.save()
        product.save()
        return cart

    def remove_to_cart(self, uid) -> bool:
        product = Product.objects.get(id=uid)
        cart = Cart.objects.get(user__id=self.pk)
        if not product or product not in self.products_buyed:
            return False
        product.cart_id = -1
        product.selling = True
        product.cart = None
        cart.total_price -= product.price
        cart.save()
        product.save()
        return True


class Cart(models.Model):

    class State(models.TextChoices):
        SHOPPING = 'SH', 'shopping'
        PAYING = 'PY', 'paying'
        FINISHED = 'FI', 'finished'
        REFUNDED = 'RF', 'refunded'

    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.PROTECT)
    total_price = models.FloatField(default=0)
    state = models.CharField(max_length=2, choices=State.choices, default=State.SHOPPING)

    def __str__(self):
        products = Product.objects.filter(cart_id=self.pk)
        len_price = len(products)
        if len_price > 0:
            return f'{self.pk} Cart is in {self.state} with {len_price} product(s)'
        else:
            return f'{self.pk} Cart is in {self.state} with nothing in it'

    def update_price(self):
        products = Product.objects.filter(cart=self)
        self.total_price = 0
        for product in products:
            self.total_price += product.price

    def save(self, *args, **kwargs):
        self.update_price()
        super(Cart, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256, default='', blank=True)
    image = models.ImageField('Cover', default=None, blank=True)

    price = models.FloatField('Selling price ($)')

    pub_date = models.DateTimeField('date published', auto_now_add=True)
    selling = models.BooleanField(default=True)

    cart = models.ForeignKey(Cart, blank=True, null=True, on_delete=models.PROTECT)
    creator = models.ForeignKey(User, blank=False, null=False, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}: $ {self.price}'

    def __add__(self, other):
        return self.price + other.price
