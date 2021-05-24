import { Cookies } from 'quasar';
import axios from 'axios';

// const USER_URL = '/'

export default {

  user: {
    authenticated: false,
  },

  jwtToken: '',

  checkAuth() {
    const jwt = Cookies.get('id_token');
    if (jwt) {
      this.user.authenticated = true;
      axios.defaults.headers.common.Authorization = `JWT ${jwt}`;
      this.jwtToken = `JWT ${jwt}`;
    } else {
      this.user.authenticated = false;
    }
  },
};
