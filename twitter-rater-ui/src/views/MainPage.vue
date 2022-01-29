<template>
    <v-container >
        <v-row justify="center" align="top" class="my-16">
            <h1>Twitter profile evaluator</h1>                                
        </v-row>            
        <v-container fill-height fluid>
            <v-row align="center" justify="center">
                <v-col md="4">
                    <p>Analyze credibility of a Twitter profiles using state-of-the-art machine learning system. After evaluation, please take a minute to fill the provided feedback form.</p>
                    <v-text-field
                        v-model="searchTerm"
                        label="Profile name"
                        outlined                        
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