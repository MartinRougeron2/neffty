import gql from 'graphql-tag';

const PRODUCT_FIELDS = `
    id
    name
    description
    image
    price
    pubDate
`;

export const GET_PRODUCTS = gql`query all_products($number: Int!, $offset: Int!) {
  allProducts (number: $number, offset: $offset) {
    ${PRODUCT_FIELDS}
  }
}`;

export const ADD_TO_CART = gql`mutation addToCart($productId: Int!) {
  addToCart(productId: $productId) {
    cart {
      id
      totalPrice
      state
      productSet {
        id
        name
        image
        creator {
          id
        }
      }
    }
  }
}
`;

export const GET_CART = gql`query
{
  cart {
    id
    totalPrice
    state
    productSet {
      id
      name
      image
      price
    }
  }
}
`;

export const GET_TOKEN = gql`mutation tokenAuth($username: String!, $password: String!) {
  tokenAuth(username: $username, password: $password) {
    payload
    refreshExpiresIn
    token
  }
}
`;

export const CREATE_USER = gql`mutation createUser($email: String!, $username: String!, $password: String!) {
  createUser(email: $email, username: $username, password: $password) {
    user {
      id
    }
  }
}
`;
