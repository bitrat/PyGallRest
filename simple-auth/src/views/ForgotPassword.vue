<template>
  <div class="login-page-container">
    <div class="login-card login-card--small">
      <p class="text-center">
        <!--  <img src="/img/logo.png" class="web-logo" alt="" /> -->
      </p>
      <b-card title="Forgot Password" class="forgot-card">
        <div v-if="backIn > 0" class="error-container">
          <b-alert show variant="danger" v-if="errorMessage">
            {{ errorMessage }}
          </b-alert>

          <b-alert show variant="success" v-if="successMessage">
            {{ successMessage }}
          </b-alert>
          <br />
          <p class="text-center">
            Back to login in <strong> {{ backIn }} </strong>
          </p>
        </div>
        <b-form @submit="onSubmit" v-else>
          <b-form-group
            id="input-group-1"
            label="Email address:"
            label-for="input-1"
          >
            <b-form-input
              id="input-1"
              v-model="form.email"
              type="email"
              required
              placeholder="Enter registered email"
            ></b-form-input>
          </b-form-group>

          <b-button
            type="submit"
            variant="primary"
            block
            class="mb-4"
            :disabled="resetting"
          >
            <b-spinner small v-if="resetting"></b-spinner>
            Continue
          </b-button>

          <p>
            <b-link to="login">Back to login</b-link>
          </p>
        </b-form>
      </b-card>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import * as types from "../store/types";
import authService from "../services/auth";

export default {
  data() {
    return {
      form: {
        email: ""
      },
      resetting: false,
      errorMessage: "",
      successMessage: "",
      backIn: -1
    };
  },
  computed: {
    ...mapGetters({
      isLoggedIn: types.IS_LOGGED_IN
    })
  },

  mounted() {
    if (this.isLoggedIn) {
      this.$router.push("/dashboard");
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();

      this.resetting = true;
      authService
        .forgotPassword(this.form)
        .then(res => {
          //this.successMessage = res.data.message;
		  this.successMessage = res.data;
          this.errorMessage = "";
        })
        .catch(e => {
          //this.errorMessage = e.response.data.message;
		  this.errorMessage = e.response.data;
          this.successMessage = "";
        })
        .finally(() => {
          this.resetting = false;
          this.backIn = 5;
        });
    }
  },

  watch: {
    backIn: function(newVal) {
      if (newVal > 0) {
        setTimeout(() => {
          this.backIn--;
        }, 1000);
      } else {
        this.$router.push("/login");
      }
    }
  }
};
</script>
