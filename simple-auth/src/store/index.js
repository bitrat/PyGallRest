import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import actions from "./actions";
import getters from "./getters";
import mutations from "./mutations";

import auth from "./modules/auth";

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    pageTitle: ""
  },
  getters,
  mutations,
  actions,
  modules: {
    auth
  },
  plugins: [createPersistedState()]
});
