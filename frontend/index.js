import Vue from 'vue';
import VueRouter from 'vue-router';

import App from './components/App.vue';
import Sites from './components/Pages/Sites.vue';
import Site from './components/Pages/Site.vue';

Vue.use(VueRouter);

fetch("/structure.json").then(function (response) {
    response.json().then(function (structure) {

        var routes = [{ path: '/', component: Sites }];
        for (var site_folder in structure) {
            routes.push({
                path: '/' + site_folder,
                component: Site
            })
        }

        const router = new VueRouter({
            mode: 'history',
            routes: routes
        });

        new Vue({
            el: '#app',
            render: h => h(App),
            router
        })
    });
});