<template>
    <div>
        <b-button @click="getStudents">Get Students</b-button>
        <div>{{ errorMessage }}</div>
        <b-table sticky-header :items="items" head-variant="light"></b-table>
    </div>
</template>

<script>

import { mapState } from 'vuex'

export default {
    name: "AcademicPerformance",
    data () {
        return {
            items: [
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' },
              { heading1: 'table cell', heading2: 'table cell', heading3: 'table cell' }
            ]
        }
    },
    computed: {
        ...mapState({
            errorMessage: state => state.errorMessage
        }),
    },
    methods: {
        getStudents() {
            this.$store.dispatch('getStudents');
        }
    }
}


</script>


<style>

</style>
