import Vue from 'vue'
import Vuex from 'vuex'
import { authenticate, getGroups,         getStudents, /*getCourses,*/ setToken, addAbsenteeism, removeAbsenteeism } from '../api/index.js'
import router from '../router/index.js'
import moment from 'moment'
Vue.use(Vuex)

var res = {
    data: {
        courses: [
            {
                id: 324,
                order: 1,
                groups: [
                    {
                        id: 456,
                        name: '1.1',
                        subjects: [
                            {
                                id: 3,
                                name: 'История'
                            },
                            {
                                id: 4,
                                name: 'Мат.Ан'
                            },
                            {
                                id: 5,
                                name: 'Информатика'
                            }
                        ],
                    },
                    {
                        id: 457,
                        name: '1.2',
                        subjects: [
                            {
                                id: 3,
                                name: 'История'
                            },
                            {
                                id: 4,
                                name: 'Мат.Ан'
                            },
                            {
                                id: 5,
                                name: 'Информатика'
                            }
                        ],
                    },
                    {
                        id: 458,
                        name: '2',
                        subjects: [
                            {
                                id: 3,
                                name: 'История'
                            },
                            {
                                id: 4,
                                name: 'Мат.Ан'
                            },
                            {
                                id: 5,
                                name: 'Информатика'
                            }
                        ],
                    }
                ],
            },
            {
                id: 325,
                order: 2,
                groups: [
                    {
                        id: 459,
                        name: '1.1',
                        subjects: [
                            {
                                id: 13,
                                name: 'Экономика'
                            },
                            {
                                id: 9,
                                name: 'ОС'
                            },
                            {
                                id: 14,
                                name: 'АиСД'
                            }
                        ],
                    },
                    {
                        id: 460,
                        name: '1.1_it',
                        subjects: [
                            {
                                id: 13,
                                name: 'Экономика'
                            },
                            {
                                id: 9,
                                name: 'ОС'
                            },
                            {
                                id: 15,
                                name: 'Комп.Графика'
                            }
                        ],
                    }
                ]
            },
        ],
        students: [
            {
                id: 2134,
                name: "Alex Red",
                dates: [
                    moment('2018-04-10'),
                    moment('2018-02-13'),
                    moment('2018-03-07'),
                ]
            },
            {
                id: 2234,
                name: "Dominic Raider",
                dates: [

                ]
            },
            {
                id: 2243,
                name: "John Lenon",
                dates: [

                ],
            },
        ],
    }
}

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
            console.log(data);
            state.courses[data.course] = data.groups.map((group) => {
                return {
                    text: group.number,
                    value: group.id,
                }
            });
            //if (!data.groups.length)
                state.courses[data.course].push({ text: 'Нет групп!', value: -1 })

            console.log(state.courses);
        },
        setStudents(state, data) {
            state.students = data.students;
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
      getGroups(context, course) {
          return getGroups(course)
            .then(res => {
                context.commit('setGroups', { course: course.course, groups: res.data.groups });
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            });
      },


      getStudents(context, groupData) {
          if (debug) {
              context.commit('setStudents', res.data);
              return;
          }

          context.commit('setTitle', groupData);
          return getStudents(groupData)
            .then(res => {
                context.commit('setStudents', res.data);
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            });
      },
      /*getCourses(context) {
          if (debug) {
              context.commit('setCourses', res.data);
              return;
          }
          getCourses()
            .then(res => {
                context.commit('setCourses', res.data);
            })
            .catch(err => {
                context.commit('setErrorMessage', err);
            })
      },*/
      addAbsenteeism(context, abs) {
          let student = context.state.students.find((stud) => stud.id == abs.studentId)
          let isExists = false;
          if (student) {
              student.dates.find(date => {
                  date = moment(date).format('DD-MM-YYYY');
                  if (date == abs.date) {
                      context.commit('setErrorMessage', 'Студент уже имеет пропуск в заданный день');
                      isExists = true;
                  }
              });
          }

          if (isExists) return;

          return addAbsenteeism(abs)
            .then(res => {
                if (res.data.status) {
                    //let student = context.state.students.find((stud) => stud.id == abs.studentId)
                    if (student) {
                        student.dates.push(res.data.date)
                    }
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
                    let student = context.state.students.find((stud) => stud.id == abs.studentId)
                    if (student) {
                        let findDate = null;
                        student.dates.find(date => {
                            console.log(abs.date, moment(date).format('DD-MM-YYYY'));
                            if (abs.date == moment(date).format('DD-MM-YYYY'))
                                findDate = date;
                        });
                        if (findDate)
                            student.dates.splice(student.dates.indexOf(findDate), 1);
                    }
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
