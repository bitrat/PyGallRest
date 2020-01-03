import axios from "axios";

export default {	
    login(payload) {
		return axios.post("http://localhost:5000/postLogin",payload,{headers :  {'Content-Type': 'application/json'}})
  },
	register(payload) {
		return axios.post("http://localhost:5000/postRegister",payload,{headers :  {'Content-Type': 'application/json'}})
  },
  	forgotPassword(payload) {
		return axios.post("http://localhost:5000/rqForgotPassword",payload,{headers :  {'Content-Type': 'application/json'}})
  },
	changePassword(token,payload) {
		return axios.post(`http://localhost:5000/change-password/${token}`,payload,{headers :  {'Content-Type': 'application/json'}})
  } 
  
};

