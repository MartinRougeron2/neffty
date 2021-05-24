import datetime

import graphql_jwt

import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import *

import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        marketplace_user = User(
            pseudo=username,
            first_name="",
            last_name="",
            email=email,
            user_dj=user
        )
        marketplace_user.save()
        return CreateUser(user=user)


class ProductObjectType(DjangoObjectType):
    class Meta:
        model = Product


class CartObjectType(DjangoObjectType):
    class Meta:
        model = Cart


class UserObjectType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "pseudo")


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductObjectType, number=graphene.Int(), offset=graphene.Int())
    cart = graphene.Field(CartObjectType)

    def resolve_all_products(self, info, **args):
        offset = args.get("offset", 0)
        product_number = args.get("number", 20) + offset
        return Product.objects.filter(selling=True).order_by('-id')[offset: product_number]

    def resolve_cart(self, info, **args):
        user_dj = info.context.user
        user = User.objects.get(user_dj=user_dj)
        cart, is_create = Cart.objects.get_or_create(user=user)
        cart.save()
        return cart


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        price = graphene.Int()
        image_url = graphene.String()
        user_id = graphene.Int()

    product = graphene.Field(lambda: ProductObjectType)

    def mutate(self, info, user_id, name, price, description="", image_url=""):
        user = User.objects.get(id=user_id)
        new_product = Product.objects.create(
            price=price,
            pub_date=datetime.datetime.today(),
            image=image_url,
            description=description,
            name=name,
            creator=user
        )
        new_product.save()
        return CreateProduct(product=new_product)


class AddToCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int()

    cart = graphene.Field(lambda : CartObjectType)

    def mutate(self, info, product_id):
        user_dj = info.context.user
        user = User.objects.get(user_dj=user_dj)
        return AddToCart(
            cart=user.add_to_cart(uid=product_id)
        )


class PayMeBaby(graphene.Mutation):
    is_all_paid = graphene.Boolean()

    def mutate(self, info, **kwargs):
        user = info.context.user
        cart = Cart.objects.filter(user=user).get(state='SH')
        products = Product.objects.filter(cart=cart)
        for product in products:
            address_donate = product.creator
            address_receive = user


class RemoveFromCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int()
        buyer_id = graphene.Int()

    is_added = graphene.Boolean()

    def mutate(self, info, product_id, user_id):
        user = User.objects.get(id=user_id)
        return AddToCart(
            is_added=user.remove_to_cart(uid=product_id)
        )


class Mutation(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
    remove_to_cart = RemoveFromCart.Field()
    create_product = CreateProduct.Field()
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema_marketplace = graphene.Schema(query=Query, mutation=Mutation)
