<template>
  <div>
  <!-- <v-app> -->
    <!-- hide when screens are larger than md -->
    <!-- <v-navigation-drawer v-model="sidebar" app d-sm-none>
      <v-list
        dense
        nav
      >
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path"
        >
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer> -->

    <v-toolbar class="px-4 my-n2" flat>
      <!-- hide icon on screens larger than md, show on screens <= md -->
      <span class="d-md-none"> 
        <v-app-bar-nav-icon @click="sidebar = !sidebar">
        </v-app-bar-nav-icon>
      </span>
      <router-link to="/">
        <v-img 
          src="/tls_logo.png" 
          class="mr-2" 
          max-height="30"
          max-width="30"
        />
      </router-link>
      <v-toolbar-title class="accent--text text-h5 appTitle">
        <router-link to="/" tag="span">
          {{ appTitle }}
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <!-- hide toolbar items when screens are smaller than md, ie show when screens are >= md breakpoint -->
      <v-toolbar-items class="d-none d-md-block">
        <v-btn
          v-for="item in menuItems"
          :key="item.title"
          text
          :to="item.path"
          active-class="navSelected"
          class="accent--text text-h6">
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
  <!-- </v-app> -->
  </div>
</template>

<script>


export default {
  name: "App",
  data(){
    return {
      appTitle: 'SocialListeners',
      sidebar: false,
      menuItems: [
          { title: 'Dashboard', path: '/dashboard'},
          { title: 'Social Media Feed', path: '/social-media-feed'},
    ]
    }
  },
};
</script>
<style scoped>
/* .navSelected {
  color: var(--v-primary-base);
  text-decoration: underline;
  text-decoration-color: #4734C2;
  background-color: white;
} */

.appTitle {
  cursor: pointer;
}

</style>
