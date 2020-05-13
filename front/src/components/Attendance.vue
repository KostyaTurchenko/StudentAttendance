<template>
    <div>
        <div class="top-panel">
            <b-button @click="$bvModal.show('get-students-modal')">Получить список студентов</b-button>
            <div class="title">Предмет:</div>
            <b-form-select v-model="course" :options="local_courses" class="" @change="changeCourse">
            </b-form-select>
            <div class="title">{{ title }}</div>
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
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: "Attendance",
    data () {
        return {
            course: null,
            group: null,
            title: "",
        }
    },
    computed: {
        ...mapState({
            courses: state => state.courses,
        }),
        local_courses() {
            return Object.keys(this.courses);
        },
        /*local_groups() {
            return
        }*/
    },
    methods: {
        changeCourse(value) {
            this.group = null;

            if (this.courses[value].length)
                this.group = this.courses[value][0].value;
            else
                this.$store.dispatch('getGroups', { course: value });
        },
        getStudents(bvModalEvt) {
            bvModalEvt.preventDefault();

            if (this.course && this.group != -1 && this.group != null) {
                setTimeout(() => {
                    this.$bvModal.hide('get-students-modal');
                }, 10);

                this.title = `Курс: ${this.course} / Группа: ${this.courses[this.course].find((group) => group.value == this.group).text}`;
            }
        }
    },
    mounted() {
        this.$bvModal.show('get-students-modal');
    },
}
</script>

<style>
.top-panel {
    display: grid;
    grid-template-columns: 30vh min-content 30vh 1fr;
    grid-gap: 0.5vh;
}

.top-panel .title {
    margin-left: 1vh;
    font-size: 1.3em;
    line-height: 1.8em;
}

</style>
