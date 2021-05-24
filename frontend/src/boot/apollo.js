import { ApolloClient } from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import VueApollo from 'vue-apollo';
import { ApolloLink, concat } from 'apollo-link';
import fetch from 'unfetch';
import log from 'loglevel';
import auth from './auth';

function BACKEND_HOST() {
  if (!process.env.PROD) {
    return 'http://127.0.0.1:8000/';
  }
  return '';
}

const baseUrl = BACKEND_HOST();

const httpLink = new HttpLink({
  uri: `${baseUrl}graphql`,
  credentials: 'include',
  fetch: (uri, options) => fetch(uri, options),
});

const authMiddleware = new ApolloLink((operation, forward) => {
  // add the authorization to the headers
  auth.checkAuth();
  operation.setContext({
    headers: {
      Authorization: auth.jwtToken,
    },
  });
  return forward(operation);
});

// Create the apollo clients
const apolloClient = new ApolloClient({
  link: concat(authMiddleware, httpLink),
  cache: new InMemoryCache(),
  connectToDevTools: true,
});

// leave the export, even if you don't use it
export default ({ app, Vue }) => {
  log.debug('install Apollo plugin');
  // Install the vue plugin
  Vue.use(VueApollo);
  const apolloProvider = new VueApollo({
    clients: {
      default: apolloClient,
    },
    defaultClient: apolloClient,
  });
  app.apolloProvider = apolloProvider;
};

export { baseUrl };
