import Vue from 'vue'
import VueRouter from 'vue-router'
import MainPage from '@/views/MainPage'
import ProfilePage from '@/views/ProfilePage'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Main',
        component: MainPage
        },
        {
        path: '/profile',
        name: 'Profile',    
        component: ProfilePage
        }
]

const router = new VueRouter({
  routes
})

export default router
