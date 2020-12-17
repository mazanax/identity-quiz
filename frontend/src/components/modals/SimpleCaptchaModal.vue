<template>
  <b-modal
      v-model="show"
      id="simple-captcha"
      :title="lang === 'ru' ? 'Подтвердите, что вы не робот' : 'Confirm that you are not robot'"
      @ok="handleOk"
      :ok-disabled="!loaded"
      :cancel-title="lang === 'ru' ? 'Отмена' : 'Cancel'"
      @show="reset">
    <div v-if="loaded">
      <div v-if="lang === 'ru'">
        <b-card bg-variant="light">Мы должны убедиться, что вы действительно человек. <!--
      -->Многие роботы пытаются выдать себя за человека, чтобы испортить нашу статистику.
        </b-card>
        <div class="my-4 text-center">Введите число, которое вы видете перед собой на экране.</div>
      </div>
      <div v-else>
        <b-card bg-variant="light">We have to make sure that you are really human. <!--
      -->Many robots try to pass themselves off as human to mess up our statistics.
        </b-card>

        <div class="my-4 text-center">Please type the number you see.</div>
      </div>

      <form method="post" @submit="handleOk">
        <h1 class="display-2 text-center">{{ question }}</h1>

        <b-form-input v-model="text"
                      id="simple-captcha-code"
                      :state="textValid"
                      :placeholder="lang === 'ru' ? 'Пожалуйста, введите число' : 'Please type the number you see'"/>
        <b-form-invalid-feedback id="simple-captcha-code-feedback">
          {{ lang === 'ru' ? 'Неверный ответ' : 'Invalid answer' }}
        </b-form-invalid-feedback>
      </form>
    </div>
    <div v-else>
      <b-skeleton width="85%"></b-skeleton>
      <b-skeleton width="55%"></b-skeleton>
      <b-skeleton width="70%"></b-skeleton>
    </div>
  </b-modal>
</template>

<script>
import {api} from "@/api";

export default {
  name: "SimpleCaptchaModal",
  props: ["lang", "value"],
  data() {
    return {
      code: '',
      loaded: false,
      text: '',
      textValid: null,
      question: ''
    }
  },
  computed: {
    show: {
      get() {
        return this.value === 0;
      },
      set() {
        this.$emit('input', this.textValid ? 1 : null);
      }
    }
  },
  methods: {
    reset() {
      this.code = '';
      this.text = '';
      this.textValid = null;
      this.loaded = false;

      api.makeRequest('GET', '/captcha')
          .catch((err) => {
            console.error(err);

            const errMessage = this.lang === 'ru'
                ? 'Произошла ошибка при запросе капчи'
                : 'There was an error when requesting the captcha';

            this.$bvToast.toast(errMessage, {
              noCloseButton: true,
              autoHideDelay: 2000,
              variant: 'danger',
              solid: true,
            })

            setTimeout(() => {
              location.reload();
            }, 2000);

            throw err;
          })
          .then(r => r.json())
          .then(json => {
            this.question = json.question;
            this.code = json.code;
            this.loaded = true;
          });
    },
    handleOk(event) {
      event.preventDefault();
      this.textValid = null;

      if (!this.text.length) {
        this.textValid = false;
        return false;
      }

      api.makeRequest('POST', '/captcha', {'body': JSON.stringify({'code': this.code, 'answer': this.text})})
          .catch((err) => {
            if (err.status !== 418) {
              throw err;
            }
          })
          .then(() => {
            this.textValid = true;

            setTimeout(() => {
              this.$bvModal.hide('simple-captcha');
            }, 400);
          })
          .catch((err) => {
            console.error(err);
            this.reset();
            this.textValid = false;
          });
    }
  }
}
</script>

<style scoped>

</style>