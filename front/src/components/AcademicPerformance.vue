<template>
    <div>
        <div class="error">{{ errorMessage }}</div>
        <div v-if="title">Курс: <b>{{ title.course.label }}</b> / Группа: <b>{{ title.group.label }}</b> / Предмет: <b>{{ title.subject.label }}</b></div>
        <b-table :items="students" :fields="studFields" striped>
            <template v-slot:cell(show_details)="row">
               <b-button size="sm" @click="row.toggleDetails" class="mr-2">
                 {{ row.detailsShowing ? 'Скрыть' : 'Показать'}}
               </b-button>
               <b-button size="sm" variant="success" @click="showAddSkip(row.item)">
                   Добавить Пропуск
               </b-button>
            </template>

            <template v-slot:row-details="row">
                <b-table :items="row.item.dates" :fields="datesFields" :dark="true">
                    <template v-slot:cell(actions)="row2">
                         <b-button size="sm" variant="danger" @click="handleRemoveAbsenteeism(row2.item, row.item.id)">
                            X
                        </b-button>
                    </template>
                </b-table>
            </template>
        </b-table>

        <b-button @click="$bvModal.show('get-students-modal')">Получить список студентов</b-button>

        <b-modal
            id="get-students-modal"
            title="Получить посещаемость студентов"
            @ok="getStudents"
        >
            <b-form>
                <b-form-group
                    label="Курс:"
                >
                    <b-form-select v-model="localId.course" :options="local_courses"/>
                </b-form-group>
                <b-form-group
                    v-if="localId.course != null"
                    label="Группа:"
                >
                    <b-form-select v-model="localId.group" :options="local_courses[localId.course].groups"/>
                </b-form-group>
                <b-form-group
                    v-if="localId.group != null"
                    label="Предмет:"
                >
                    <b-form-select v-model="localId.subject" :options="local_courses[localId.course].groups[localId.group].subjects"/>
                </b-form-group>
            </b-form>
        </b-modal>

        <b-modal
            id="add-skip"
            :title="addSkipTitle"
            @ok="handleAddSkip"
        >
            <b-form-datepicker v-model="date"></b-form-datepicker>
        </b-modal>
    </div>
</template>

<script>

import { mapState } from 'vuex'
import moment from 'moment'

export default {
    name: "AcademicPerformance",
    data () {
        return {
            localId: {
                course: null,
                group: null,
                subject: "tset",
            },
            studFields: [
                {
                    key: "name",
                    label: "Имя"
                },
                {
                    key: "amount",
                    label: "Пропуски"
                },
                {
                    key: "show_details",
                    label: "Действия"
                }
            ],
            datesFields: [
                {
                    key: "view",
                    label: "Даты пропусков"
                },
                {
                    key: "actions",
                    label: "Действия"
                }
            ],
            currentStudent: null,
            date: "",
        }
    },
    computed: {
        ...mapState({
            courses: state => state.courses,
            title: state => state.title,
            students: state => state.students.map(obj => { return {
                ...obj,
                amount: obj.dates.length,
                _showDetails: false,
                dates: obj.dates.map(date => {return {
                    ...date,
                    view: moment(date).format('DD-MM-YYYY'),
                }})
            }}),
            errorMessage: state => state.errorMessage,

        }),
        local_courses() {
            return this.courses.map((course, index) => {
                return {
                    ...course,
                    value: index,
                    text: course.order,
                    groups: (!course.groups) ? [] : course.groups.map((group, index) => {
                        return {
                            ...group,
                            value: index,
                            text: group.name,
                            subjects: (!group.subjects) ? [] : group.subjects.map((subject, index) => {
                                return {
                                    ...subject,
                                    value: index,
                                    text: subject.name,
                                }
                            })
                        }
                    }),
                }
            })
        },
        addSkipTitle() {
            if (this.currentStudent)
                return `Добавить пропуск ${this.currentStudent.name}`
            return ''
        }
    },
    methods: {
        checkGetStudentsFormValid() {
            for (let key in this.localId) {
                if (this.localId[key] == null) {
                    return false;
                }
            }

            return true;
        },
        getStudents(bvModalEvt) {
            bvModalEvt.preventDefault();
            if (!this.checkGetStudentsFormValid())
                return;
            this.$store.dispatch('getStudents', {
                course: {
                    id: this.local_courses[this.localId.course].id,
                    label: this.local_courses[this.localId.course].order,
                },
                group: {
                    id: this.local_courses[this.localId.course].groups[this.localId.group].id,
                    label: this.local_courses[this.localId.course].groups[this.localId.group].name,
                },
                subject: {
                    id: this.local_courses[this.localId.course].groups[this.localId.group].subjects[this.localId.subject].id,
                    label: this.local_courses[this.localId.course].groups[this.localId.group].subjects[this.localId.subject].name,
                }
            });
            setTimeout(() => {
                this.$bvModal.hide('get-students-modal');
            }, 10)
        },
        showAddSkip(currentStudent) {
            this.currentStudent = currentStudent;
            this.$bvModal.show('add-skip');
        },
        handleAddSkip(bvModalEvt) {
            bvModalEvt.preventDefault();
            if (!this.date)
                return;

            this.$store.dispatch('addAbsenteeism', {
                date: moment(this.date).format('DD-MM-YYYY'),
                studentId: this.currentStudent.id,
                subject: this.local_courses[this.localId.course].groups[this.localId.group].subjects[this.localId.subject].id,
            });
            this.currentStudent = null;
            this.date = null;
            setTimeout(() => {
                this.$bvModal.hide('add-skip');
            }, 10)
        },
        handleRemoveAbsenteeism(date, studentId) {
            //console.log(date);
            this.$store.dispatch('removeAbsenteeism', {
                date: date.view,
                studentId: studentId,
                subject: this.local_courses[this.localId.course].groups[this.localId.group].subjects[this.localId.subject].id,
            });
        }
    },
    mounted() {
        this.$bvModal.show('get-students-modal');
        this.$store.dispatch('getCourses');
    }
}


</script>


<style scoped>
.error {
    color: red;
}
</style>
