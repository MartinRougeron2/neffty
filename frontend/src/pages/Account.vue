<template>
  <q-page class="row justify-center">
    <div v-if="!isAuth" class="col-9 q-pt-xl">
      <q-form
        @submit="onSubmit"
        @reset="onReset"
        class="q-gutter-md shadow-13 q-pa-xl"
      >
        <q-input
          filled
          type="email"
          v-model="email"
          label="email"
          lazy-rules
          :disable="!create"
          :rules="[ val => create && val && val.length > 0 || 'Please type something']"
        />
        <q-input
          filled
          v-model="username"
          label="Username"
          lazy-rules
          :rules="[ val => val && val.length > 0 || 'Please type something']"
        />

        <q-input
          filled
          type="password"
          v-model="password"
          label="Password"
          lazy-rules
          :rules="[ val => val && val.length > 0 || 'Please type something']"
        />
        <q-toggle
          v-model="create"
          color="green"
          label="Create account"
        />

        <div class="row justify-between">
          <q-btn class="col-5" :label="create ? 'Create' : 'Login'" type="submit"
                 color="secondary"/>
          <q-btn class="col-4 q-pa-md" label="Reset" type="reset" color="secondary" flat/>
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script>

import auth from 'boot/auth';

import { GET_TOKEN, CREATE_USER } from 'src/constants/graphql';
import { Cookies, Notify } from 'quasar';
import axios from 'axios';

export default {
  name: 'Account',
  data() {
    return {
      username: '',
      password: '',
      email: '',
      create: false,
      isAuth: auth.user.authenticated,
    };
  },
  methods: {
    onSubmit() {
      this.login();
    },
    onReset() {
      this.username = '';
      this.password = '';
    },
    login() {
      this.$apollo.mutate({
        mutation: GET_TOKEN,
        variables: {
          username: this.username,
          password: this.password,
        },
      })
        .then((response) => {
          Cookies.set('id_token', response.data.tokenAuth.token, { path: '/' });
          axios.defaults.headers.common.Authorization = `JWT ${Cookies.get('id_token')}`;
          Cookies.set('username', this.username, { path: '/' });
          this.jwtToken = `JWT ${Cookies.get('id_token')}`;
          this.$router.push('/');
        })
        .catch(() => {
          Notify.create({
            message: 'Bad credentials',
            color: 'negative',
          });
          this.username = '';
          this.password = '';
        });
    },
    createAccount() {
      this.$apollo.mutate({
        mutation: CREATE_USER,
        variables: {
          username: this.username,
          password: this.password,
        },
      })
        .then(() => {
          this.login();
        })
        .catch(() => {
          Notify.create({
            message: 'Bad credentials',
            color: 'negative',
          });
        });
    },
  },
};
</script>

<style scoped>

</style>
