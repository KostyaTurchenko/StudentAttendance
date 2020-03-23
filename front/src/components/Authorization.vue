<template>
    <div id="authorization">
        <center><h3>Авторизация</h3></center>
        <b-form @submit="onSubmit" v-if="show">
            <b-form-group
                id="input-group-1"
                label="Логин:"
                label-for="input-1"
                label-align="left"
            >
                <b-form-input
                    id="input-1"
                    v-model="form.login"
                    type="text"
                    required
                    placeholder="Введите логин"
                >
                </b-form-input>
            </b-form-group>
            <b-form-group
                id="input-group-2"
                label="Пароль:"
                label-for="input-2"
                label-align="left"
            >
                <b-form-input
                    id="input-2"
                    v-model="form.password"
                    type="password"
                    required
                    placeholder="Введите пароль"
                >
                </b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Войти</b-button>
        </b-form>
        <div id="errMsg">{{ errorMessage }}</div>
    </div>
</template>

<script>

import { mapState } from 'vuex'

export default {
    name: "Authorization",
    data() {
        return {
            show: true,
            form: {
                login: '',
                password: '',
            },
            message: "Hello Students!!!",
        }
    },
    computed: {
        ...mapState({
            errorMessage: state => state.errorMessage
        }),
    },
    methods: {
        onSubmit (evt) {
            evt.preventDefault()
            this.$store.dispatch('login', { login: this.form.login, password: this.form.password })
        },
    }
}

</script>

<style scoped>
#authorization {
    margin-top: 30px;
    margin-left: 50%;
    transform: translate(-50%);
    width: 300px;
}

#errMsg {
    color: red;
}
</style>
