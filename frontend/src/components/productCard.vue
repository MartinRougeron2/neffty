<template>
  <q-card class="q-ma-md q-pa-sm shadow-8">
    <img v-if="itemToShow.image"
         :src="backend_url + 'media/' + itemToShow.image" alt="Illustration">
    <img v-else :src="backend_url + 'media/' + 'Neffty_2.png'" alt="Illustration">

    <q-card-section>
      <div class="text-h6">{{ itemToShow.name }}</div>
      <div class="text-subtitle2">by John Doe</div>
    </q-card-section>
    <q-separator/>
    <q-card-actions class="q-pt-sm q-gutter-sm" align="between">
      <q-avatar>
        $ {{ itemToShow.price }}
      </q-avatar>
      <q-btn round class="q-mt-sm" color="primary" icon="shopping_cart"
             @click="addToCart(itemToShow)" :disable="!isAuth"/>
    </q-card-actions>
    <q-inner-loading :showing="loading.includes(itemToShow.id)">
      <q-spinner-gears size="50px" color="primary"/>
    </q-inner-loading>
  </q-card>
</template>

<script>

import { baseUrl } from 'boot/apollo';
import auth from '../boot/auth';

export default {
  props: {
    itemToShow: Object,
    loading: Array,
  },
  name: 'product-card',
  methods: {
    addToCart(item) {
      console.log(item);
      this.$root.$emit('addToCartFromProduct', item);
    },
  },
  data() {
    return {
      backend_url: baseUrl,
      isAuth: auth.user.authenticated,
    };
  },
};
</script>

<style scoped>

</style>
