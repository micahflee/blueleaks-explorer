import Vue from 'vue';
import VueRouter from 'vue-router';

import App from './components/App.vue';
import Structure from './components/Pages/Structure.vue';
import StructureEdit from './components/Pages/StructureEdit.vue';
import Sites from './components/Pages/Sites.vue';
import Site from './components/Pages/Site.vue';
import Table from './components/Pages/Table.vue';
import Item from './components/Pages/Item.vue';

const routes = [
    { path: '/', component: Sites },
    { path: '/structure', component: Structure },
    { path: '/structure/:site', component: StructureEdit },
    { path: '/:site', component: Site },
    { path: '/:site/:table', component: Table },
    { path: '/:site/:table/:id', component: Item },
];

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    mode: 'history',
    routes
});

Vue.createApp(App).use(router).mount('#app')