<template>
    <v-container fluid align="start">
        <v-row justify="center" align="start">            
                <h1>{{ username }}</h1>                            
        </v-row>
        <v-row justify="center" class="mt-16" fill-height>
            <v-col md=5 class="mt-6">
                <v-card elevation="2" >
                    <v-row>
                        <v-img
                        class="ma-4"
                        max-height="250"
                        max-width="250"
                        :src="profile_pic"
                        ></v-img>
                        <v-col class="ma-4" align="left">
                            <h3>Profile name</h3>         
                            <div class="mt-8">
                                <p>Profile desctiption here</p>                            
                                <p>Other info about the profile here if there is any</p>                                

                            </div>                                        
                        </v-col>
                    </v-row>
                    <v-row class="mx-16">
                        <v-col align="left">
                            <h2>Score 1:</h2>
                        </v-col>
                        <v-col align="right">
                            <h2>5.5</h2>
                        </v-col>
                    </v-row>
                    <v-divider class="mx-16"></v-divider>
                    <v-row class="mx-16">
                        <v-col align="left">
                            <h2>Score 2:</h2>
                        </v-col>
                        <v-col align="right">
                            <h2>7.4</h2>
                        </v-col>
                    </v-row>
                </v-card> 
            </v-col>
            <v-col md=5>
                <div v-for="tweet in tweets" :key="tweet">
                    <Tweet :id="tweet" :options="{conversation : 'None', cards: 'hidden'}"></Tweet>
                </div>
            </v-col>
        </v-row>

    </v-container>
</template>

<script>
import { Tweet } from 'vue-tweet-embed'
    export default {
        name: "ProfilePage",
        components: {
            Tweet,
        },
        data() {
            return {
                username: "Test user",
                profile_pic: require('@/assets/profile_default.jpg'),
                tweets: [
                    "1481256002741755905",
                    "1481188837665742848",
                    "1479475073241260036"
                ]
            }
        },

    }
</script>

<style lang="scss" scoped>

</style>