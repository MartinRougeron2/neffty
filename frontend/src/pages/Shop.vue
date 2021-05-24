<template>
  <q-page class="row justify-center">
    <div class="q-mt-md col-10">
      <q-input label="Search an item" v-model="searchQuery"/>
    </div>
    <div class="q-pt-xl row justify-between col-10">
      <div class="col-4" v-for="item in itemList" :key="item.id">
        <product-card :itemToShow="item" :loading="load"/>
      </div>
    </div>
  </q-page>
</template>

<script>

import productCard from 'components/productCard';

import { GET_PRODUCTS } from '../constants/graphql';

export default {
  name: 'Shop',
  components: {
    productCard,
  },
  data() {
    return {
      searchQuery: '',
      itemList: [],
      load: [],
    };
  },
  created() {
    this.fetchItems();
    this.$root.$on('addToCartFromProduct', (item) => {
      setTimeout(this.fetchItems, 2000);
      this.$root.$emit('addToCartFromShop', item);
      this.itemList.filter((item_) => item_.id !== item.id);
      this.load.push(item.id);
    });
    this.$root.$on('addToCartFromProductAdded', (id) => {
      let it = {};
      this.itemList.forEach((item) => {
        if (item.id === id) {
          it = item;
        }
      });
      this.itemList.splice(it, 1);
      this.load.splice(id, 1);
    });
    setInterval(this.fetchItems, 10000);
  },
  methods: {
    ShowCart() {
      this.$root.$emit('showCart');
    },
    fetchItems() {
      this.$apollo.query({
        query: GET_PRODUCTS,
        variables: {
          number: 10,
          offset: 0,
        },
      })
        .then((result) => {
          this.itemList = result.data.allProducts;
        });
    },
  },
};

</script>

<style scoped>

</style>
