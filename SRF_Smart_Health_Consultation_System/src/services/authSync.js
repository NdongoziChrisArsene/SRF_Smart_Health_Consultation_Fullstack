let store;

export const injectStore = (_store) => {
  store = _store;
};

export const reduxLogout = () => {
  if (store) {
    store.dispatch({ type: "auth/logout" });
  }
};

export const reduxUpdateAccessToken = (token) => {
  if (store) {
    store.dispatch({ type: "auth/updateAccessToken", payload: token });
  }
};
