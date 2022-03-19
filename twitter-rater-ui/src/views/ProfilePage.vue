<template>
    <v-container fluid align="start">
        <v-row justify="center" align="top" class="mt-16">            
            <v-col>
                <h1>{{ username }}</h1>                            
                <p>Your credibility score was computed using a simple Machine Learning algorithm that takes into account several factors of your profile, and also incorporates your latest tweets as input.</p>                            
            </v-col>
        </v-row>
        <v-row justify="center" align="start">            
                
        </v-row>
        <v-row justify="center" class="mt-8" fill-height>
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
                            <h2>{{ scores.score }}/10</h2>
                        </v-col>
                    </v-row>
                    <v-divider class="mx-16"></v-divider>
                    <div>
                         <v-row class="my-8">
                            <v-col>
                                <h3>The following properties had the greatest effect on your score. Positives increased the score, while negatives decreased the score.</h3>
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
                                <v-col align="right" v-if="showPartial">
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
                                <v-col align="right" v-if="showPartial">
                                    <h2>{{ score.contribution }}</h2>
                                </v-col>
                            </v-row>
                            <v-divider class="mx-16"></v-divider>
                        </div>
                    </div>
                </v-card> 
                <v-row class="mt-16">
                    <v-col align="left">
                        <a :href="feedbackLink" @click.prevent="feedbackClick">
                            <h1>Fill in the final questionnaire</h1>
                        </a>
                        <p class="">By filling in the questionnaire, you will help researchers.</p>

                    </v-col>
                </v-row>
            </v-col>
            <v-col md=5>
                <div v-if="pinnedTweet">
                    <h3 v-if="index == 0" align="left">Pinned</h3>
                    <Tweet :id="pinnedTweet" :options="{conversation : 'None', cards: 'hidden'}"></Tweet>
                </div>
                <div v-for="(tweet, index) in tweets" :key="index">
                    <Tweet :id="tweet" :options="{conversation : 'None', cards: 'hidden'}"></Tweet>
                </div>
                <div v-if="(!tweets || tweets.length == 0) && !pinnedTweet">
                    <h3 align="left">This user has no tweets. This may affect evaluation</h3>
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
                            window.open(this.feedbackLink, '_blank');                            
                        
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
            pinnedTweet(){
                return this.profile?.pinned_tweet_id ? this.profile?.pinned_tweet_id : null
            },
            tweets(){
                let temp = []
                if(this.profile?.tweets){                    
                    for(let i = 0; i < 3; i++){
                        if(this.profile.tweets[i])
                            temp.push(this.profile.tweets[i].id)
                    }
                }
                return temp
            },
            scores(){
                return this.profile?.ml_output ? {...this.profile.ml_output.explanations, score: this.profile.ml_output.score} : {score: 0}
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