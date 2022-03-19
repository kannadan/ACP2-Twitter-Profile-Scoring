<template>
    <v-container >
        <v-row justify="center" align="top" class="my-16">
            <h1>Evaluate your Twitter profile credibility!</h1>                                
        </v-row>            
        <v-container  fluid>
            <v-row align="center" justify="center" >
                <v-col md="4" class="pa-0">
                    <p>Analyse your Twitter profile’s credibility using a tool created by researchers at the University of Oulu, Finland. Type your Twitter username without the @-mark in the textbox below and click the button to let us compute your credibility score. By filling in a short questionnaire study after observing the score and the properties that affect it, you will help researchers build better tools for understanding online social media and critical reading.</p>
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
                            User profile was not found or it was unsuitable for evaluation. Check your spelling or try another account
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
                    <h3 class="pt-6">Disclaimer</h3>
                    <h4>By proceeding to use this application, you consent to being a subject in a study by team of researchers from University of Oulu. Your Twitter information (only public accounts), results, and feedback will be stored. The collected Twitter information is limited to public data available via Twitter API. The stored data will be deleted after the study.</h4>
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
            },
            verifyData(profile){
                return !!profile && !!profile.ml_output
            }
    }
}
</script>

<style lang="scss" scoped>

</style>