<template>
  <div>
    <q-list class="row justify-center">
      <q-card v-for="item in cart.productSet" :key="item.id"
              class="col-10 q-ma-sm shadow-8">
        <q-img v-if="item.image" :src="backend_url + 'media/' + item.image"/>
        <q-img v-else :src="backend_url + 'media/' + 'Neffty_2.png'"/>
        <q-card-section class="text-white bg-primary">
          <p class="text-h4 text-bold text-center">
            {{ item.name }}
          </p>
          <p class="text-right text-h6">
            $ {{ item.price }}
          </p>
        </q-card-section>
      </q-card>
    </q-list>
    <q-footer class="bg-secondary">
      <div class="q-pa-md">
          <div class="text-white text-h5 row justify-between">
            <div class="text-white">
              Total:
            </div>
              <div class="text-right">
                $ {{ cart.totalPrice}}
              </div>
          </div>
      </div>
    </q-footer>
  </div>
</template>

<script>

import { baseUrl } from 'boot/apollo';

export default {
  props: {
    cart: Object,
  },
  name: 'cart',
  data() {
    return {
      backend_url: baseUrl,
    };
  },
};
</script>

<style scoped>

</style>
