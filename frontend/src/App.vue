<template>
  <b-container id="app">
    <b-row class="justify-content-md-center">
      <b-col sm="12" md="8" class="mt-4">
        <div class="text-center">
          <b-img :src="img" alt="Logo" fluid class="logo"/>
        </div>

        <h1 class="text-center my-5">{{ lang === 'ru' ? 'Кто ты?' : 'Who are you?' }}</h1>
      </b-col>

      <Quiz v-if="loaded && (!voted || !auth)" :lang="lang" :auth="auth"/>
      <Results v-if="loaded && auth && voted" :lang="lang"/>
      <Auth v-if="loaded" :lang="lang" :auth="auth" :name="name"/>
      <b-col v-else sm="12" md="8">
        <b-skeleton width="85%"></b-skeleton>
        <b-skeleton width="55%"></b-skeleton>
        <b-skeleton width="70%"></b-skeleton>
      </b-col>

      <b-col sm="12" md="8" class="text-center mt-5 small">
        <a href="/privacy" target="_blank">Политика конфиденциальности</a>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Quiz from "@/components/Quiz";
import Auth from "@/components/Auth";
import Results from "@/components/Results";

import img from "../public/logo.jpg";
import {api} from "@/api";

export default {
  name: 'App',
  components: {Quiz, Auth, Results},
  mounted() {
    this.lang = location.pathname === '/en' ? 'en' : 'ru';

    api.makeRequest("GET", "/user", {'noReload': true})
      .catch(response => {
        if (response.status === 401) {
          this.auth = false;
          this.voted = false;
          this.loaded = true;
        }

        throw response;
      })
      .then(response => response.json())
      .then(json => {
        this.auth = true;
        this.loaded = true;
        this.voted = json.step === 3;
        this.name = json.name;
        this.lang = json.lang;

        if (location.pathname !== '/' + json.lang) {
          history.replaceState(null, '', '/' + json.lang);
        }
      })
      .catch(response => {
        if (response.status !== 401) {
          console.error(response);
        }
      });
  },
  data() {
    return {
      lang: '',
      loaded: false,
      name: null,
      auth: true,
      voted: false,
      img: img
    }
  },
  computed: {
    step: {
      get() {
        return this.$store.state.step;
      },
      set(step) {
        this.$store.commit('setStep', step);
      }
    }
  }
}
</script>
