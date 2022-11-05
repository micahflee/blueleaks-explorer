import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue';
import Structure from './Pages/Structure.vue';
import StructureEdit from './Pages/StructureEdit.vue';
import Sites from './Pages/Sites.vue';
import Site from './Pages/Site.vue';
import Table from './Pages/Table.vue';
import Item from './Pages/Item.vue';

const routes = [
    { path: '/', component: Sites },
    { path: '/structure', component: Structure },
    { path: '/structure/:site', component: StructureEdit },
    { path: '/:site', component: Site },
    { path: '/:site/:table', component: Table },
    { path: '/:site/:table/:id', component: Item },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

const app = createApp(App)
app.use(router)
app.mount('#app')