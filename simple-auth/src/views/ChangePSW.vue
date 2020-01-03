<template>
  <div class="login-page-container">
    <div class="login-card">
      <p class="text-center">
      <!--  <img src="/img/logo.png" class="web-logo" alt="" /> -->
      </p>
      <b-card no-body class="overflow-hidden">
        <b-row no-gutters>
          <b-col md="6" class="login-card__left">
            <div class="text-center m-3">
              <h2 class="mt-5">Instruction</h2>
              <p>
				<b>Change password</b> - Enter your e-mail address and set a new password.
              </p>
			  <p>
			  <b>PLEASE NOTE:</b> There is an, up to 10 second delay, between entering your new password and receiving a result - this is due to the verification process.
			  </p>
            </div>
          </b-col>
          <b-col md="6" class="login-card__right">
            <b-card-body title="Change password">
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
                    placeholder="Enter email"
                  ></b-form-input>
                </b-form-group>
				
                <b-form-group
                  id="input-group-2"
                  label="Password:"
                  label-for="input-2"
                >
                  <b-form-input
                    type="password"
                    id="input-2"
                    v-model="form.password"
                    required
                    placeholder="Enter password"
                  ></b-form-input>
                </b-form-group>

                <b-form-group
                  id="input-group-3"
                  label="Verify Password:"
                  label-for="input-3"
                >
                  <b-form-input
                    type="password"
                    id="input-3"
                    v-model="form.verifyPassword"
                    required
                    placeholder="Enter password again"
                  ></b-form-input>
                </b-form-group>

                <b-button
                  type="submit"
                  variant="primary"
                  block
                  class="mb-4"
                  :disabled="change"
                >
                  <b-spinner small v-if="change"></b-spinner>
                  Change Password
                </b-button>
                <p>
                  Remembered your password?
                  <b-link to="login">Login</b-link>
                </p>
              </b-form>
            </b-card-body>
          </b-col>
        </b-row>
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
        email: "",
		//code: "",
        password: "",
        verifyPassword: "",
		tokenVerify: ""
      },
      change: false,
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

	  this.tokenVerify = this.$route.params.token

      if (this.form.password !== this.form.verifyPassword) {
        this.errorMessage = "The passwords you entered didn't match - go back to your email and click on the Password reset link again";
        this.backIn = 8;
        return;
      }

      this.change = true;
      authService
        .changePassword(this.tokenVerify, this.form)
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
          this.change = false;
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
