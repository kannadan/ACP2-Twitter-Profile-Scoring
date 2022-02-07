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
                        class="my-8 mx-16 profile-pic"
                        max-height="75"
                        max-width="75"
                        :src="profile_pic"
                        ></v-img>
                        <v-col class="ma-4" align="left">
                            <h3>{{ username }}</h3>         
                            <div class="mt-8">
                                <p>{{ description }}</p>                            
                                <!-- <p>Other info about the profile here if there is any</p>-->
                                <p>{{ location }}</p>
                            </div>                                        
                        </v-col>
                    </v-row>
                    <v-row class="mx-16">
                        <v-col>
                            Following: {{ following }}
                        </v-col>
                        <v-col>
                            Followers: {{ followers }}
                        </v-col>
                    </v-row>
                    <v-row class="mx-16" v-if="scores">
                        <v-col align="left">
                            <h2>Total score:</h2>
                        </v-col>
                        <v-col align="right">
                            <h2>{{ scores.score }}/5</h2>
                        </v-col>
                    </v-row>
                    <v-divider class="mx-16"></v-divider>
                    <div v-if="showPartial">
                         <v-row class="my-8">
                            <v-col>
                                <h3>Parial scores are calculated separetely from total score to show points of improvement</h3>
                            </v-col>                            
                        </v-row>
                        <v-row class="mx-16 mt-8 green-text">
                            <v-col align="left">    
                                <h1 color="green">Positives</h1>
                            </v-col>
                        </v-row>
                        <div v-for="(score, index) in scores.positives" :key="index" class="green-text">
                            <v-row class="mx-16" >
                                <v-col align="left">
                                    <h2>{{ score.name }}</h2>
                                </v-col>
                                <v-col align="right">
                                    <h2>{{ score.contribution }}</h2>
                                </v-col>
                            </v-row>
                            <v-divider class="mx-16"></v-divider>
                        </div>
                        <v-row class="mx-16 mt-8 red-text">
                            <v-col align="left">    
                                <h1>Negatives</h1>
                            </v-col>
                        </v-row>
                        <div v-for="(score, index) in scores.negatives" :key="index + 3" class="red-text">
                            <v-row class="mx-16" >
                                <v-col align="left">
                                    <h2>{{ score.name }}</h2>
                                </v-col>
                                <v-col align="right">
                                    <h2>{{ score.contribution }}</h2>
                                </v-col>
                            </v-row>
                            <v-divider class="mx-16"></v-divider>
                        </div>
                    </div>
                </v-card> 
                <v-row class="mt-16">
                    <a :href="feedbackLink" @click.prevent="feedbackClick">
                        <h1>Please give feedback</h1>
                    </a>
                </v-row>
            </v-col>
            <v-col md=5>
                <div v-for="(tweet, index) in tweets" :key="index">
                    <h3 v-if="index == 0" align="left">Pinned</h3>
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
                apiUrl: process.env.VUE_APP_API_URL,
                profile: {},
                profile_pic_static: require('@/assets/profile_default.jpg'),
                showPartial: false,
                feedbackLink: "https://docs.google.com/forms/d/e/1FAIpQLScK4zOm5n0znSx1sM4Wg6wFG88FMqfjDvaN60vzV6NQVLNjTQ/viewform?usp=pp_url&entry.786300512=",
                userId: 0,
                requestOptions: {
                    method: "POST",
                    // mode: 'no-cors',
                    headers: { "Content-Type": "application/json",
                                "Accept": "application/json",
                                "Access-Control-Allow-Origin": "*" ,
                                "Access-Control-Allow-Credentials": "true",
                                "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"},
                    body: ''
                }
            }
        },
        methods: {
            listenForFocusFilterShortcut (event) {
                if (event.keyCode === 74 && event.altKey) {
                    this.showPartial = !this.showPartial
                } 
            },
            feedbackClick(){
                console.log("CLICK")
                this.profile.userId = this.userId
                this.requestOptions.body = JSON.stringify(this.profile)
                fetch(this.apiUrl + "SaveResults", this.requestOptions)
                    .then(response => {
                        console.log(response)
                        if(response.status == 201)
                            window.location.href = this.feedbackLink
                        
                    })
                    .catch((e) => {
                        console.log("Error", e)
                    });
            }
        },
        computed: {
            username(){
                return this.profile ? this.profile.name : ""
            },
            description(){
                return this.profile ? this.profile.description : ""
            },
            location(){
                return this.profile ? this.profile.location : ""
            },
            profile_pic(){
                return this.profile ? this.profile.profile_image_url : this.profile_pic_static
            },
            followers(){
                return this.profile ? this.profile.public_metrics.followers_count : 0
            },
            following(){
                return this.profile ? this.profile.public_metrics.following_count : 0
            },
            tweets(){
                let temp = []
                if(this.profile){
                    temp.push(this.profile.pinned_tweet_id)
                    for(let i = 0; i < 3; i++){
                        temp.push(this.profile.tweets[i].id)
                    }
                }
                return temp
            },
            scores(){
                return this.profile ? {...this.profile.ml_output.explanations, score: this.profile.ml_output.score} : {}
            },
        },
        created(){
            this.profile = this.$store.state.profile
            if(Object.keys(this.profile).length === 0 ){                
                this.$router.push({ name: 'Main'})
            }
            this.userId = new Date().getTime()
            this.feedbackLink = this.feedbackLink + this.userId
            window.addEventListener(
                'keyup',
                this.listenForFocusFilterShortcut
            )
        },
        beforeDestroy(){
            window.removeEventListener('keyup', this.listenForFocusFilterShortcut);            
        }
    }
</script>

<style lang="scss" scoped>
.profile-pic {
  border-radius: 50%;
}

.green-text {
    color: green
}
.red-text {
    color: red
}

</style>