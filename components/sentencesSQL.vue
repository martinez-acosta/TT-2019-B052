<template>
  <div class="container">
    <div class="row col">
      <v-toolbar dense>
        <v-btn icon>
          <v-icon>mdi-content-save</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>mdi-content-paste</v-icon>
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon>mdi-help</v-icon>
        </v-btn>
      </v-toolbar>
    </div>
    <div class="row col">
      <code class="container border">
        {{ sentences }}
      </code>
    </div>
  </div>
</template>

<script type="module">
export default {
  data() {
    return {
      sentences: `
      CREATE TABLE [IF NOT EXISTS] table_name(
        column_1_definition,
        column_2_definition,
        ...,
        table_constraints
        ) ENGINE=storage_engine;
      `
    }
  }
}
</script>
