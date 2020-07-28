<style scoped>
.meta {
  color: #333333;
  font-style: italic;
}
</style>

<template>
  <div>
    <template v-if="loading">
      <div class="loading">
        <img src="/static/loading.gif" alt="Loading" />
      </div>
    </template>
    <template v-else>
      <h2>
        <i class="fas fa-sitemap"></i>
        <router-link v-bind:to="linkToSite">{{ siteName }}</router-link>
      </h2>
      <h3>
        <i class="fas fa-table"></i>
        {{ tableName }}
      </h3>
      <div class="meta">Displaying {{ numberWithCommas(count) }} rows</div>
      <ul class="rows">
        <li v-for="row in rows" class="row" v-bind:key="row[0]">
          <TableRow
            v-bind:siteFolder="siteFolder"
            v-bind:table="table"
            v-bind:row="row"
            v-bind:importantFields="importantFields"
            v-bind:hiddenFields="hiddenFields"
            v-bind:fieldTypes="fieldTypes"
            v-bind:headers="headers"
          ></TableRow>
        </li>
      </ul>
      <template v-if="count">
        <Paging
          v-bind:totalItems="count"
          v-bind:perPageCount="perPageCount"
          v-bind:offset="offset"
          v-bind:pageNavigateHandler="pageNavigateHandler"
        ></Paging>
      </template>
    </template>
  </div>
</template>

<script>
import TableRow from './TableRow.vue';
import Paging from './Paging.vue';

export default {
  data: function() {
    return {
      loading: false,
      siteFolder: this.$route.path.split('/')[1],
      table: this.$route.path.split('/')[2],
      siteName: null,
      tableName: null,
      headers: null,
      rows: null,
      count: null,
      importantFields: null,
      hiddenFields: null,
      fieldTypes: null,
      offset: 0,
      perPageCount: 50
    };
  },
  created: function() {
    this.getRows();
  },
  methods: {
    getRows: async function() {
      this.loading = true;
      // console.log(`count: ${this.perPageCount} offset: ${this.offset}`);
      try {
        const response = await fetch(
          `/api/${this.siteFolder}/${this.table}?count=${this.perPageCount}&offset=${this.offset}`
        );
        if (response.status !== 200) {
          this.loading = false;
          console.log('Error fetching rows, status code: ' + response.status);
          return;
        }
        const data = await response.json();

        this.siteName = data['site_name'];
        this.tableName = data['table_name'];
        this.headers = data['headers'];
        this.rows = data['rows'];
        this.count = data['count'];
        this.importantFields = data['important_fields'];
        this.fieldTypes = data['field_types'];

        // Fill in the hidden fields
        this.hiddenFields = [];
        for (var i in this.headers) {
          if (!this.importantFields.includes(this.headers[i])) {
            this.hiddenFields.push(this.headers[i]);
          }
        }

        // Fill in the default field types
        for (var i in this.headers) {
          if (!this.fieldTypes[this.headers[i]]) {
            this.fieldTypes[this.headers[i]] = 'text';
          }
        }

        this.loading = false;
      } catch (err) {
        this.loading = false;
        console.log('Error fetching rows', err);
      }
    },
    numberWithCommas: function(x) {
      if (!x) return '...';
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    pageNavigateHandler: function(page) {
      this.offset = this.perPageCount * (page - 1);
      this.getRows();
    }
  },
  computed: {
    linkToSite: function() {
      return '/' + this.siteFolder;
    }
  },
  components: {
    TableRow,
    Paging
  }
};
</script>
