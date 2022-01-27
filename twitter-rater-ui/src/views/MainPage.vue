<template>
    <v-container fill-height fluid>
        <v-row justify="center" align="top">
            <v-col>
                <h1>Twitter profile evaluator</h1>                

            </v-col>

        </v-row>
        <v-row align="center" justify="center">
            <v-col md="4">
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum</p>
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
                searchTerm: "",
                apiUrl: process.env.VUE_APP_API_URL
            }
        },
        methods: {
            getProfile(){
                console.log("Profile search " + this.searchTerm + " " + this.apiUrl)
                fetch(this.apiUrl + "GetProfile?username=" + this.searchTerm)
                    .then(response => response.json())
                    .then((data) => {                                             
                        if(data)
                            this.$store.commit('setProfile', data)                            
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