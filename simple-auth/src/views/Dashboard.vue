<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand to="/dashboard">Request Access</b-navbar-brand>
      
	  <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
         <!-- <b-nav-item to="/dashboard/page1">Page1</b-nav-item> -->
         <!-- <b-nav-item to="/dashboard/page2">Page2</b-nav-item> -->
         <!-- <b-nav-item to="/dashboard/page3">Page3</b-nav-item> -->
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              <em>{{ loggedUserEmail }}</em>
            </template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
            <b-dropdown-item href="#" @click="signOutNow"
              >Sign Out</b-dropdown-item
            >
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-container class="text-center mt-5">
      <b-alert show variant="success">
        Logged in successfully!
      </b-alert>
      <p>
        <b>A Mobile Credential has been sent to your cellphone</b>
	  </p>
	  <p>
		Please check your cellphone for further instructions on gaining Access.
	  </p>
	  <p>
       	<br />
        Back to login in <strong> {{ backIn }} </strong>
      </p>
    </b-container>

    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import * as types from "../store/types";

export default {
  data() {
    return {
      backIn: -1
    };
  },
  computed: {
    ...mapGetters({
      isLoggedIn: types.IS_LOGGED_IN,
      loggedUserEmail: types.EMAIL
    })
  },

  mounted() {
    if (!this.isLoggedIn) {
      this.$router.push("/login");
    }

    this.backIn = 5;
  },
  methods: {
    ...mapActions({
      logout: types.LOGOUT
    }),
    signOutNow() {
      this.logout();
      this.$router.push("/login");
    }
  },
  watch: {
    backIn: function(newVal) {
      if (newVal > 0) {
        setTimeout(() => {
          this.backIn--;
        }, 1000);
      } else {
        this.signOutNow();
      }
    }
  }
};
</script>
