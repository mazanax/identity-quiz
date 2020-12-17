<template>
  <b-col sm="12" md="8" class="mt-5 text-center">
    <b-card v-if="!auth" bg-variant="light">
      {{ lang === 'ru'
        ? 'Чтобы принять участие в опросе, вы должны авторизоваться, используя один из доступных сервисов.'
        : 'To take part in the survey, you must log in using one of the available services.' }}
      <div class="d-flex justify-content-center my-3">
        <b-btn class="btn-social d-flex align-items-center justify-content-center" @click="doFbAuth">
          <b-img :src="facebookIcon" class="social-icon"/>
        </b-btn>
        <b-btn class="btn-social d-flex align-items-center justify-content-center" @click="doVkAuth">
          <b-img :src="vkIcon" class="social-icon"/>
        </b-btn>
        <b-btn class="btn-social d-flex align-items-center justify-content-center" @click="doGoogleAuth">
          <b-img :src="googleIcon" class="social-icon"/>
        </b-btn>
      </div>

      <small class="mt-3">
        {{ lang === 'ru'
          ? 'Мы не используем ваши данные в маркетинговых целях, не анализируем и не передаем третьим лицам.'
          : 'We do not use your data for marketing purposes, we do not analyze it or share it with third parties.'}}
      </small>
    </b-card>
    <div v-else class="mb-4">
      <p>{{ lang === 'ru' ? 'Привет' : 'Hello' }}, {{ name }}!</p>
      <a href="javascript://" @click="logout()">{{ lang === 'ru' ? 'Выйти' : 'Log Out' }}</a>
    </div>
  </b-col>
</template>

<script>
import vk from '../assets/icons/vk.png'
import fb from '../assets/icons/fb.png'
import google from '../assets/icons/google.png'

export default {
  name: "Auth",
  props: ["auth", "lang", "name"],
  data() {
    return {
      window: null,
      facebookIcon: fb,
      vkIcon: vk,
      googleIcon: google,
    }
  },
  methods: {
    doVkAuth() {
      console.log('VK auth');
      const API_HOST = process.env.VUE_APP_SITE_HOST;
      const CLIENT_ID = process.env.VUE_APP_VK_CLIENT_ID;

      this.openAuthWindow(`https://oauth.vk.com/authorize?client_id=${CLIENT_ID}&display=popup&response_type=code&v=5.126&redirect_uri=${API_HOST}/auth/vk`, this.lang === 'ru' ? 'Войти с помощью ВКонтакте' : 'Login with VK');
    },
    doFbAuth() {
      console.log('FB auth');
      const API_HOST = process.env.VUE_APP_SITE_HOST;
      const CLIENT_ID = process.env.VUE_APP_FB_CLIENT_ID;

      this.openAuthWindow(`https://www.facebook.com/v9.0/dialog/oauth?client_id=${CLIENT_ID}&state=RANDOM_STRING&redirect_uri=${API_HOST}/auth/facebook`, this.lang === 'ru' ? 'Войти с помощью Facebook' : 'Login with Facebook');
    },
    doGoogleAuth() {
      console.log('GOOGLE auth');
      const API_HOST = process.env.VUE_APP_SITE_HOST;
      const CLIENT_ID = process.env.VUE_APP_GOOGLE_CLIENT_ID;
      const scope = 'https://www.googleapis.com/auth/userinfo.profile'

      this.openAuthWindow(`https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${API_HOST}/auth/google&scope=${scope}`, this.lang === 'ru' ? 'Войти с помощью Google' : 'Login with Google')
    },
    openAuthWindow(url, name) {
      this.window = window.open(url, name, 'width=800, height=600, resizable=no, status=no, location=no, toolbar=no, menubar=no')
    },
    logout() {
      localStorage.removeItem('token');

      const errMessage = this.lang === 'ru'
          ? 'Вы успешно вышли с сайта'
          : 'You successfully logged out';

      this.$bvToast.toast(errMessage, {
        noCloseButton: true,
        autoHideDelay: 2000,
        variant: 'success',
        solid: true,
      })

      setTimeout(() => {
        location.reload();
      }, 2000);
    }
  }
}
</script>

<style scoped>

</style>