<style scoped>
.label {
  font-weight: bold;
}

.html-value {
  background-color: white;
  max-width: 100%;
  max-height: 600px;
  overflow: auto;
}

ul {
  list-style: none;
  padding: 0;
}

li.join {
  margin-bottom: 1em;
  padding: 1em;
  background-color: #ddeaf5;
  border: 1px solid #c9d4dd;
}
</style>

<template>
  <div>
    <template v-if="loading">
      <div class="loading">
        <img src="/static/loading-small.gif" alt="Loading" />
      </div>
    </template>
    <template v-else>
      <template v-if="join">
        <span class="label">{{ join['name'] }}:</span>
        <ul class="join-rows">
          <li v-for="joinRow in joinRows" class="join">
            <JoinRow
              v-bind:site="site"
              v-bind:table="joinTable"
              v-bind:row="joinRow"
              v-bind:fields="joinFields"
              v-bind:headers="joinHeaders"
            ></JoinRow>
          </li>
        </ul>
      </template>
      <template v-else>
        <template v-if="value != ''">
          <span class="label">{{ field['name'] }}:</span>
          <span v-if="field['type'] == 'text'">{{ value }}</span>
          <span v-else-if="field['type'] == 'pre'">
            <pre>{{ preValue(value) }}</pre>
          </span>
          <span v-else-if="field['type'] == 'html'">
            <div class="html-value" v-html="htmlValue(value)"></div>
          </span>
          <span v-else-if="field['type'] == 'image'">
            <img v-bind:src="attachmentUrl(value)" />
          </span>
          <span v-else-if="field['type'] == 'attachment'">
            <a v-bind:href="attachmentUrl(value)" target="_blank">{{
              value
            }}</a>
          </span>
          <span v-else>Unimplemented field type: {{ field['type'] }}</span>
        </template>
      </template>
    </template>
  </div>
</template>

<script>
import JoinRow from './JoinRow.vue';

export default {
  props: ['site', 'table', 'itemId', 'field', 'value', 'join'],
  data: function() {
    return {
      loading: false,
      joinTable: null,
      joinHeaders: null,
      joinRows: null,
      joinCount: null,
      joinFields: null
    };
  },
  created: function() {
    if (this.join) {
      this.getJoin();
    }
  },
  methods: {
    getJoin: function() {
      var that = this;
      this.loading = true;
      fetch(
        '/api/' +
          this.site +
          '/' +
          this.table +
          '/join/' +
          this.join['name'] +
          '/' +
          this.itemId
      )
        .then(function(response) {
          if (response.status !== 200) {
            that.loading = false;
            console.log(
              'Error fetching join rows, status code: ' + response.status
            );
            return;
          }
          response.json().then(function(data) {
            that.loading = false;
            that.joinTable = data['join_table'];
            that.joinHeaders = data['join_headers'];
            that.joinRows = data['join_rows'];
            that.joinCount = data['join_count'];
            that.joinFields = data['join_fields'];
          });
        })
        .catch(function(err) {
          that.loading = false;
          console.log('Error fetching join rows', err);
        });
    },
    stripScripts: function(htmlString) {
      const div = document.createElement('div');
      div.innerHTML = htmlString;
      const scripts = div.getElementsByTagName('script');
      let i = scripts.length;
      while (i--) {
        scripts[i].parentNode.removeChild(scripts[i]);
      }

      const base = div.getElementsByTagName('base');
      i = base.length;
      while (i--) {
        base[i].parentNode.removeChild(base[i]);
      }

      return div.innerHTML;
    },
    htmlValue: function(value) {
      return this.stripScripts(value)
        .replace(/\\n/g, ' ')
        .replace(/\\t/g, ' ')
        .replace(/POSITION: absolute;/g, '')
        .replace(/position:absolute;/g, '');
    },
    preValue: function(value) {
      return value.replace(/\\n/g, '\n');
    },
    attachmentUrl: function(value) {
      var url =
        '/blueleaks-data/' + this.site + '/files/' + value.replace('\\', '/');
      return url;
    }
  },
  components: {
    JoinRow: JoinRow
  }
};
</script>
