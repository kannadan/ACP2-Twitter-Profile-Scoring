<template>
    <v-container fill-height fluid>
        <v-row align="center" justify="center">
            <v-col md="4">
                <v-text-field
                    v-model="searchTerm"
                    label="Profile name"
                    outlined
                    >
                </v-text-field>
                <v-btn color="primary" @click="getProfile">
                    Evaluate profile
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: "MainPage",
        data() {
            return {
                searchTerm: ""
            }
        },
        methods: {
            getProfile(){
                console.log("Profile search " + this.searchTerm)
                fetch("http://192.168.1.108:5000/api/GetProfile?username=" + this.searchTerm)
                    .then(response => response.json())
                    .then((data) => {
                        console.log(data)
                        if(data)
                            this.$router.push("Profile")
                    })
                    .catch((e) => {
                        console.log("Error", e)
                    })
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>