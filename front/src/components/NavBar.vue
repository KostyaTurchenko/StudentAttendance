<template>
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item href="/">Home</b-nav-item>
                    <b-nav-item href="/authorization" :disabled='isAuthenticated'>Login</b-nav-item>
                    <!--<b-nav-item href="/performance" :disabled='!isAuthenticated'>Успеваемость</b-nav-item>-->
                    <b-nav-item href="/attendance" :disabled='!isAuthenticated'>Посещаемость</b-nav-item>
                </b-navbar-nav>

                <b-navbar-nav class="ml-auto">
                    <b-nav-item-dropdown right v-if="isAuthenticated">
                        <template v-slot:button-content>
                            <span>{{ userName }}</span>
                        </template>
                        <b-dropdown-item @click="signOut" href="#">Sign Out</b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
import { mapMutations } from 'vuex'


export default {
    name: "Navbar",
    data() {
        return {
            show: false,
        }
    },
    computed: {
        userName() {
            return `${this.$store.state.userData.name} ${this.$store.state.userData.surname}`;
        },
        isAuthenticated() {
            return this.$store.getters.isAuthenticated
        }
    },
    methods: {
        ...mapMutations([
            'signOut',
        ]),
    }
}

</script>
