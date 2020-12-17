<template>
  <b-col sm="12" md="8" class="my-2 d-flex justify-content-end">
    <b-nav small>
      <b-nav-item :disabled="lang === 'ru'" @click="setLang('ru')">Русский</b-nav-item>
      <b-nav-item :disabled="lang === 'en'" @click="setLang('en')">English</b-nav-item>
    </b-nav>
  </b-col>
</template>

<script>
import {api} from "@/api";

export default {
  name: "LangSelector",
  props: ["lang"],
  methods: {
    setLang(lang) {
      if (localStorage.getItem('token')) {
        api.makeRequest('PATCH', '/user', {'body': JSON.stringify({'lang': lang}), 'noReload': true})
            .catch(response => {
              if (response.status !== 401) {
                throw response;
              }
            })
            .then(() => {
              location.href = `/${lang}`;
            })
      } else {
        location.href = `/${lang}`;
      }
    }
  }
}
</script>

<style scoped>

</style>