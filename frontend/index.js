import Vue from 'vue';
import VueRouter from 'vue-router';

import App from './components/App.vue';
import Structure from './components/Pages/Structure.vue';
import Sites from './components/Pages/Sites.vue';
import Site from './components/Pages/Site.vue';
import Table from './components/Pages/Table.vue';
import Item from './components/Pages/Item.vue';

Vue.use(VueRouter);

fetch("/structure.json").then(function (response) {
    response.json().then(function (structure) {

        var routes = [
            { path: '/', component: Sites },
            { path: '/structure', component: Structure },
        ];
        for (var site_folder in structure) {
            routes.push({
                path: '/' + site_folder,
                component: Site
            });
            for (var table in structure[site_folder]["tables"]) {
                routes.push({
                    path: '/' + site_folder + "/" + table,
                    component: Table
                });
                routes.push({
                    path: '/' + site_folder + "/" + table + "/:id",
                    component: Item
                });
            }
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
