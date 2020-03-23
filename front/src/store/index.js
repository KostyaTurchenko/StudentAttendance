import Vue from 'vue'
import Vuex from 'vuex'
import { authenticate, getStudents } from '../api/index.js'
import router from '../router/index.js'
Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        errorMessage: '',
        userData: {
            name: localStorage.getItem('name'),
            surname: localStorage.getItem('surname'),
        },
        jwt: {
            token: localStorage.getItem('token'),
        }
    },
    getters: {
        isAuthenticated (state) {
            let token = state.jwt.token;

            if (!token || token.split('.').length < 3) {
              return false;
            }

            const data = JSON.parse(atob(token.split('.')[1]));
            const exp = new Date(data.exp * 1000);
            const now = new Date();
            return now < exp;
        },
    },
    mutations: {
        setLocalData(state, data) {
            if (data.status == 'error') {
                state.errorMessage = "Неверный логин или пароль";
                return;
            }

            localStorage.token = state.jwt.token = data.token;
            localStorage.name = state.userData.name = data.name;
            localStorage.surname = state.userData.surname = data.surname;
            state.errorMessage = "";
            router.push('/')
        },
        signOut(state) {
            state.testMessage = state.jwt
            state.userData = {};
            state.jwt.token = '';
            localStorage.clear();
            router.push('/');
        },
        setErrorMessage(state, msg) {
            state.errorMessage = msg;
        }
    },
  actions: {
      login(context, userData) {
          return authenticate(userData)
            .then(res => {
                context.commit('setLocalData', res.data);
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            });
      },
      getStudents(context) {
          return getStudents(context.state.jwt.token)
            .then(res => {
                context.commit('setErrorMessage', res.data);
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            });
      }
  },
  modules: {
  }
})
