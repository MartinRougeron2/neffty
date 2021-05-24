<template>
  <q-layout view="hHr lpR fFf">

    <q-header reveal elevated class="bg-secondary text-white">
      <q-toolbar>
        <q-toolbar-title>
          <div class="row justify-start q-px-xl q-py-md">

            <div class="col-2">
              <q-btn round flat to="/">
                <q-avatar>
                  <img src="Neffty.png" alt="Logo">
                </q-avatar>
              </q-btn>
            </div>
            <div class="col-5">
              <q-btn flat to="/shop" label="Marketplace" size="16px"/>
            </div>
            <div class="col-5 row justify-end">
              <q-btn :label="isAuth ? name: 'account'" icon="person" flat to="/account"/>
              <q-btn label="Cart" icon="shopping_cart" flat @click="right = !right">
                <q-badge v-if="cart.productSet" floating color="primary">
                  {{ cart.productSet.length }}
                </q-badge>
              </q-btn>
            </div>
          </div>
        </q-toolbar-title>

      </q-toolbar>
    </q-header>

    <q-drawer v-model="right" side="right" behavior="mobile" elevated>
      <cart v-if="isAuth" :cart="cart"/>
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>

  </q-layout>
</template>

<script>

import cart from 'components/cart';

import { Cookies } from 'quasar';
import { ADD_TO_CART, GET_CART } from 'src/constants/graphql';
import auth from '../boot/auth';

export default {
  components: {
    cart,
  },
  data() {
    return {
      right: false,
      client: {},
      ii: 0,
      cart: {},
      cartTmp: [],
      isAuth: !!(Cookies.get('id_token')),
      name: Cookies.get('username'),
    };
  },
  methods: {
    getCart() {
      this.$apollo
        .query({
          query: GET_CART,
        })
        .then((results) => {
          if (results.data.cart) {
            this.cart = (results.data.cart);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addToCartMutation(id) {
      this.$apollo
        .mutate({
          mutation: ADD_TO_CART,
          variables: {
            productId: Number(id),
          },
        })
        .then((results) => {
          if (results.data.addToCart.cart) {
            this.cart = (results.data.addToCart.cart);
            this.$root.$emit('addToCartFromProductAdded', id);
          } else {
            this.$q.notify({
              message: 'Cannot add product to cart',
              type: 'warning',
            });
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addToCart(item) {
      this.cartTmp.push(item);
      while (this.isAuth && this.cartTmp.length) {
        this.addToCartMutation(this.cartTmp.pop().id);
      }
    },
  },
  updated() {
    this.name = Cookies.get('username');
  },
  created() {
    auth.user.authenticated = !!Cookies.get('id_token');
    this.isAuth = auth.user.authenticated;
    if (this.isAuth) {
      this.getCart();
    }

    this.$root.$on('showCart', () => {
      this.right = true;
    });
    this.$root.$on('hideCart', () => {
      this.right = false;
    });
    this.$root.$on('changeCart', () => {
      this.right = !this.right;
    });
    this.$root.$on('addToCartFromShop', (item) => this.addToCart(item));
    setInterval(this.getCart, 5000);
  },
};
</script>
