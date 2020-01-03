import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
    redirect: "/login"
  },
    {
    path: "/test",
    name: "test",
    component: () => import("../views/Test.vue")
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/Login.vue")
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/Register.vue")
  },
  {
    path: "/forgot-password",
    name: "forgot-password",
    component: () => import("../views/ForgotPassword.vue")
  },
    {
    path: "/change-password/:token",
    name: "change-password",
    component: () => import("../views/ChangePSW.vue")
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("../views/Dashboard.vue"),
    children: [
      {
        path: "/",
        component: () => import("../views/dashboard/Home.vue")
      },
      {
        path: "page1",
        component: () => import("../views/dashboard/Page1.vue")
      }
    ]
  }
];

const router = new VueRouter({
  routes,
  mode: "history"
});

export default router;
