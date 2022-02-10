<template>
    <v-container >
        <v-row justify="center" align="top" class="my-16">
            <h1>How credible are you?</h1>                                
        </v-row>            
        <v-container fill-height fluid>
            <v-row align="center" justify="center">
                <v-col md="4">
                    <h3>Disclaimer</h3>
                    <h4>By proceeding to use this application, you consent to being a subject in a study by team of researchers from University of Oulu.</h4>
                    <p>Use this tool to analyze credibility of your Twitter profile. Type your Twitter username as shown by the instruction image and press "Evaluate profile". Afterwards, please fill the provided questionnaire form, your input will be very appreciated!</p>
                    <v-text-field
                        v-model="searchTerm"
                        label="Profile name"
                        outlined
                        @keydown.enter.prevent="getProfile"                    
                        >
                    </v-text-field>
                    <v-expand-transition>
                        <v-alert                    
                        color="red"
                        dark
                        v-if="error"
                        >
                            User profile was not found. Check your spelling or try another account
                        </v-alert>
                    </v-expand-transition>
                    <v-btn color="primary" @click="getProfile" style="width: 185px" :disabled="loading">
                        <div v-if="!loading">Evaluate profile</div>
                        <v-progress-circular
                            v-else
                            indeterminate
                            color="green"
                        ></v-progress-circular>
                    </v-btn>
                </v-col>
            </v-row>

        </v-container>
    </v-container>
</template>

<script>
    export default {
        name: "MainPage",
        data() {
            return {
                searchTerm: "", 
                apiUrl: process.env.VUE_APP_API_URL,
                error: false,      
                loading: false          
            }
        },
        methods: {
            getProfile(){
                console.log("Profile search " + this.searchTerm + " " + this.apiUrl)
                if(this.searchTerm){
                    this.loading = true
                    this.error = false
                    fetch(this.apiUrl + "GetProfile?username=" + this.searchTerm)
                        .then(response => {
                            this.loading = false
                            console.log("response", response)
                            return response.json()
                        })
                        .then((data) => {                 
                            if(data){
                                this.$store.commit('setProfile', data)                            
                                this.$router.push("Profile")
                            }
                            else
                                this.error = true;
                        })
                        .catch((e) => {
                            this.loading = false
                            this.error = true
                            console.log("Error", e)
                        })
                } else
                    this.error = true
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>