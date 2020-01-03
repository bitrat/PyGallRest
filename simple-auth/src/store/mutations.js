import * as types from "./types";

export default {
  [types.MUTATE_SET_PAGE_TITLE]: (state, payload) => {
    state.pageTitle = payload;
  }
};
