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
                <b>Login</b> - to receive a Mobile Credential to your cellphone's Gallagher Mobile Connect application.
				</p>
			  <p>
				<b>Register</b> - If you are entitled to register and you have not registered before, click the "Register" link, enter your e-mail address and set a password 
              </p>
			  <p>
			  <b>PLEASE NOTE:</b> There is an, up to 10 second delay, between entering information and receiving a result - this is due to the verification process.
			  </p>
            </div>
          </b-col>
          <b-col md="6" class="login-card__right">
            <b-card-body title="Login - Request Mobile Credential">
              <div v-if="backIn > 0" class="error-container">
                <b-alert show variant="danger">
                  {{ errorMessage }}
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

                <b-button
                  type="submit"
                  variant="primary"
                  block
                  class="mb-4"
                  :disabled="loggingIn"
                >
                  <b-spinner small v-if="loggingIn"></b-spinner>
                  Login
                </b-button>

                <b-row>
                  <b-col md="6">
                    <p>
                      <b-link to="register">Register</b-link>
                    </p>
                  </b-col>
                  <b-col md="6">
                    <p>
                      <b-link to="forgot-password">Forgot password</b-link>
                    </p>
                  </b-col>
                </b-row>
              </b-form>
            </b-card-body>
          </b-col>
        </b-row>
      </b-card>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import * as types from "../store/types";
import authService from "../services/auth";

export default {
  data() {
    return {
      form: {
        email: "",
        password: ""
      },
      loggingIn: false,
      errorMessage: "",
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
    ...mapActions({
      setUserInfo: types.SET_USER_INFO
    }),
    onSubmit(evt) {
      evt.preventDefault();

      this.loggingIn = true;
      authService
        .login(this.form)
        .then(res => {
          console.log(res);
          this.setUserInfo(res.data);
          this.$router.push("/dashboard");
        })
        .catch(e => {
          console.log(e);
          this.errorMessage = e.response.data;
          this.backIn = 5;
        })
        .finally(() => {
          this.loggingIn = false;
        });
      //   alert(JSON.stringify(this.form));
    }
  },

  watch: {
    backIn: function(newVal) {
      if (newVal > 0) {
        setTimeout(() => {
          this.backIn--;
        }, 1000);
      }
    }
  }
};
</script>
