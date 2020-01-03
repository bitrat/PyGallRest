import * as types from "../types";

const state = {
  isLoggedIn: false,
  email: ""
};

const getters = {
  [types.IS_LOGGED_IN]: state => {
    return state.isLoggedIn;
  },
  [types.EMAIL]: state => {
    return state.email;
  }
};

const mutations = {
  [types.MUTATE_SET_USER_INFO]: (state, payload) => {
    state.isLoggedIn = true;
    state.email = payload.email;
  },
  [types.MUTATE_LOGOUT]: state => {
    state.isLoggedIn = false;
    state.email = "";
  }
};

const actions = {
  [types.SET_USER_INFO]: ({ commit }, payload) => {
    commit(types.MUTATE_SET_USER_INFO, payload);
  },
  [types.LOGOUT]: ({ commit }, payload) => {
    commit(types.MUTATE_LOGOUT, payload);
  }
};

export default {
  state,
  mutations,
  actions,
  getters
};
