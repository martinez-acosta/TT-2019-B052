<template>
  <div class="ma-12 pa-12">
    <template>
      <v-navigation-drawer permanent app expand-on-hover clipped>
        <v-list>
          <v-list-item link>
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="title">{{
                user.name
              }}</v-list-item-title>
              <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list nav dense>
          <v-list-item link nuxt to="/workspace/files">
            <v-list-item-icon>
              <v-icon>mdi-folder</v-icon>
            </v-list-item-icon>
            <v-list-item-title>My Files</v-list-item-title>
          </v-list-item>

          <v-list-item link nuxt to="/workspace/diagram">
            <v-list-item-icon>
              <v-icon>mdi-vector-polyline-edit</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Diagram</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </template>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters({
      user: 'calls/userInfo'
    })
  }
}
</script>
