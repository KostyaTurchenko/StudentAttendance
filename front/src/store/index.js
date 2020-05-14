import Vue from 'vue'
import Vuex from 'vuex'
import { authenticate, getGroups, getSubjects, getStudents, setToken, getAllAbsenteeism, addAbsenteeism, removeAbsenteeism } from '../api/index.js'
import router from '../router/index.js'
//import moment from 'moment'
Vue.use(Vuex)

var debug = false;
export default new Vuex.Store({
    state: {
        errorMessage: '',
        userData: {
            name: localStorage.getItem('name'),
            surname: localStorage.getItem('surname'),
        },
        jwt: {
            token: localStorage.getItem('token'),
        },
        courses: {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
        },
        students: [],
        subjects: [],
        dates: [],
        title: '',
    },
    getters: {
        isAuthenticated (state) {
            if (debug)
                return true;

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
            setToken(data.token);
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

            setTimeout(() => {
                state.errorMessage = "";
            }, 10000)
        },
        setGroups(state, data) {
            state.courses[data.course] = data.groups.map((group) => {
                return {
                    text: group.number,
                    value: group.id,
                }
            });
            if (!data.groups.length)
                state.courses[data.course].push({ text: 'Нет групп!', value: -1 })
        },
        setSubjects(state, data) {
            state.subjects = data.map((subject) => {
                return {
                    value: subject.id,
                    text: subject.name,
                }
            })
        },
        setStudents(state, students) {
            state.students = students;
        },
        setDates(state, dates) {
            state.dates = dates;
            /*for (let i = 1; i < 30; i++)
                state.dates.push({
                    date: "2020-04-"+i,
                    group_id: 1,
                    student_id: 4,
                    subject_id: 1,
                    id: 3,
                })*/
        },
        addDay(state, day) {
            state.dates.push({
                date: day,
            })
        },
        addAbsenteeism(state, date) {
            state.dates.push(date);
        },
        removeAbsenteeism(state, absId) {
            let fined = state.dates.find(date => {
                return date.id == absId
            });
            fined.student_id = -1;
            /*let index = state.dates.indexOf(fined);
            state.dates.splice(index, 1);*/
        },

        setTitle(state, data) {
            state.title = data;
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
      getSubjects(context) {
          return getSubjects()
            .then(res => {
                context.commit('setSubjects', res.data.subjects)
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            })
      },
      getGroups(context, course) {
          return getGroups(course)
            .then(res => {
                context.commit('setGroups', { course: course.course, groups: res.data.groups });
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            });
      },
      getStudents(context, groupId) {
          return getStudents({ group_id: groupId })
            .then(res => {
                context.commit('setStudents', res.data.students);
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            });
      },
      getAllAbsenteeism(context, data) {
          return getAllAbsenteeism(data)
            .then(res => {
                context.commit('setDates', res.data.dates);
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            });
      },

      addAbsenteeism(context, abs) {
          return addAbsenteeism(abs)
            .then(res => {
                if (res.data.status) {
                    context.commit('addAbsenteeism', res.data.date)
                }
                //context.commit('setStudents', res.data);
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            });
      },
      removeAbsenteeism(context, abs) {
          return removeAbsenteeism(abs)
            .then(res => {
                if (res.data.status) {
                    context.commit('removeAbsenteeism', abs.absentId)
                }
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            });
      }
  },
  modules: {
  }
})
