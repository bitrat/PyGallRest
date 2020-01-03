import * as types from "./types";

export default {
  [types.SET_PAGE_TITLE]: ({ commit }, payload) => {
    commit(types.MUTATE_SET_PAGE_TITLE, payload);
  }
};
