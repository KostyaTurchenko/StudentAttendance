<template>
    <div>
        <div class="top-panel">
            <b-button @click="$bvModal.show('get-students-modal')">Получить список студентов</b-button>
            <div v-if="title" class="title">Предмет:</div>
            <b-form-select v-if="title" v-model="subject" :options="subjects" class="" @change="changeSubject">
            </b-form-select>
            <div class="title">{{ title }}</div>
            <div v-if="title" class="title small">Добавить день:</div>
            <b-button v-if="title" @click="$bvModal.show('add-day')" variant="success">+</b-button>
        </div>
        <hr />
        <div>
            <b-table class="students" responsive :fields="tableFields" :items="tableItems" bordered v-if="students.length">
                <template v-slot:cell()="data">
                    <div @click="cellClick(data)" class="m-cell">{{ (data.field.key == 'fullName') ? data.value : (data.value.date_id) ? "x" : "" }}</div>
                </template>
            </b-table>
        </div>


        <b-modal
            id="get-students-modal"
            title="Получить список студентов"
            @ok="getStudents"
        >
            <b-form>
                <b-form-group lable="Курс:">
                    <b-form-select v-model="course" :options="local_courses" class="mb-3" @change="changeCourse">
                        <template v-slot:first>
                            <b-form-select-option :value="null" disabled>-- Выберите курс --</b-form-select-option>
                        </template>
                    </b-form-select>
                </b-form-group>
                <b-form-group v-if="courses[course] && courses[course].length" lable="Группа:">
                    <b-form-select v-model="group" :options="courses[course]" class="mb-3">
                        <template v-slot:first>
                            <b-form-select-option :value="null" disabled>-- Выберите группу --</b-form-select-option>
                        </template>
                    </b-form-select>
                </b-form-group>
                <b-spinner v-if="courses[course] && !courses[course].length" variant="success" type="grow" label="Spinning"></b-spinner>
            </b-form>
        </b-modal>

        <b-modal
            id="add-absenteeism"
            title="Добавление пропуска"
            @ok="addAbsenteeism"
        >
            <div>Добавить пропуск?</div>
            <div>Дата: <b>{{ add_absenteeism.date }}</b></div>
            <div>Студент: <b>{{ add_absenteeism.studName }}</b></div>
        </b-modal>

        <b-modal
            id="remove-absenteeism"
            title="Удаление пропуска"
            @ok="removeAbsenteeism"
        >
            <div>Убрать пропуск?</div>
            <div>Дата: <b>{{ add_absenteeism.date }}</b></div>
            <div>Студент: <b>{{ add_absenteeism.studName }}</b></div>
        </b-modal>


        <b-modal
            id="add-day"
            title="Добавить день в список"
            @ok="addDay"
        >
            <b-form-datepicker v-model="day" class="mb-2"></b-form-datepicker>
        </b-modal>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import moment from 'moment'

export default {
    name: "Attendance",
    data () {
        return {
            course: null,
            group: null,
            subject: 1,
            title: "",
            day: moment(new Date()).format("YYYY-MM-DD"),
            add_absenteeism: {
                studName: "",
                studentId: null,
                date: "",
                dateId: null,
            },
        }
    },
    computed: {
        ...mapState({
            courses: state => state.courses,
            subjects: state => state.subjects,
            students: state => state.students,
            dates: state => state.dates,
        }),
        local_courses() {
            return Object.keys(this.courses);
        },
        tableItems() {
            return this.students.map((student) => {
                return {
                    id: student.id,
                    fullName: `${student.surname} ${student.name}`,
                    ...this.getDatesForStudent(student.id),
                }
            })
        },
        tableFields() {
            let dates = this.dates.map((date) => {
                return {
                    key: date.date,
                    label: moment(date.date).format('DD-MM'),
                }
            }).sort((a, b) => {
                let res = (moment(a.key) > moment(b.key)) ? 1 : -1;
                return res
            });
            return [
                { key: 'fullName', label: 'Имя' },
                ...dates,
            ]
        }
    },
    methods: {
        changeCourse(value) {
            this.group = null;

            if (this.courses[value].length)
                this.group = this.courses[value][0].value;
            else
                this.$store.dispatch('getGroups', { course: value });
        },
        changeSubject() {
            this.$store.dispatch('getAllAbsenteeism', { groupId: this.group, subjectId: this.subject });
        },
        getStudents(bvModalEvt) {
            bvModalEvt.preventDefault();

            if (this.course && this.group != -1 && this.group != null) {
                setTimeout(() => {
                    this.$bvModal.hide('get-students-modal');
                }, 10);

                this.title = `Курс: ${this.course} / Группа: ${this.courses[this.course].find((group) => group.value == this.group).text}`;

                this.$store.dispatch('getStudents', this.group);
                this.$store.dispatch('getAllAbsenteeism', { groupId: this.group, subjectId: this.subject });
            }
        },
        cellClick(data) {
            if (data.field.key == "fullName")
                return;

            this.add_absenteeism = {
                studName: data.item.fullName,
                studentId: data.item.id,
                date: data.field.key,
                dateId: (data.item[data.field.key]) ? data.item[data.field.key].date_id : -1,
            }

            if (!data.item[data.field.key]) {
                this.$bvModal.show('add-absenteeism');
            }
            else {
                this.$bvModal.show('remove-absenteeism');
            }


        },
        addAbsenteeism() {
            this.$store.dispatch('addAbsenteeism', {
                subjectId: this.subject,
                studentId: this.add_absenteeism.studentId,
                groupId: this.group,
                date: moment(this.add_absenteeism.date).format("DD-MM-YYYY"),
            });
        },
        removeAbsenteeism() {
            this.$store.dispatch('removeAbsenteeism', {
                absentId: this.add_absenteeism.dateId,
            });
        },
        addDay() {
            this.$store.commit('addDay', this.day);
        },
        getDatesForStudent(studentId) {
            let result = this.dates.filter(date => {
                return date.student_id == studentId
            }).reduce((p, c) => {
                p[c.date] = { date_id: c.id };
                return p;
            }, {});
            return result;
        },
    },
    mounted() {
        this.$store.dispatch('getSubjects');
        this.$bvModal.show('get-students-modal');
    },
}
</script>

<style>
.top-panel {
    display: grid;
    grid-template-columns: 250px min-content 180px 1fr min-content min-content;
    grid-gap: 0.5vh;
}

.top-panel .title {
    margin-left: 10px;
    font-size: 20px;
    line-height: 38px;
}

.top-panel .title.small {
    text-align: right;
    width: 130px;
    font-size: 1.1em;
    line-height: 2.2em;
}

.students td {
    padding: 0;
}

.m-cell {
    width: 100%;
    min-width: 65px;
    min-height: 40px;
    line-height: 40px;
    margin: auto;
    user-select: none;
}

</style>
