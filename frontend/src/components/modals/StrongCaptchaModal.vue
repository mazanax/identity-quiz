<template>
  <b-modal
      v-model="show"
      id="strong-captcha"
      :title="lang === 'ru' ? 'Подтвердите, что вы не робот' : 'Confirm that you are not robot'"
      @ok="handleOk"
      :ok-disabled="!loaded"
      :cancel-title="lang === 'ru' ? 'Отмена' : 'Cancel'"
      @show="reset">
    <div v-if="loaded">
      <div v-if="lang === 'ru'">
        <b-card bg-variant="light">ОК. Это было не так сложно, правда? <!--
      -->К сожалению, роботы с легкостью справляются с предыдущей задачей, поэтому усложняем задачу.
        </b-card>
        <div class="my-4 text-center">Пожалуйста, введите число с картинки.</div>
      </div>
      <div v-else>
        <b-card bg-variant="light">OK. That wasn't so hard, was it? <!--
      -->Unfortunately, robots can easily do the previous task, so let's make it harder.
        </b-card>
        <div class="my-4 text-center">Please type the text you see in the picture.</div>
      </div>

      <form method="post" @submit="handleOk">
        <div class="d-flex justify-content-center align-items-center">
          <b-img fluid :src="`data:image/jpeg;base64,${image}`" class="mb-3"/>
        </div>
        <b-form-input v-model="text"
                      id="strong-captcha-code"
                      :state="textValid"
                      :placeholder="lang === 'ru' ? 'Пожалуйста, введите код с картинки' : 'Please type the text you see in the picture'"/>
        <b-form-invalid-feedback id="strong-captcha-code-feedback">
          {{ lang === 'ru' ? 'Введен неверный код' : 'Invalid code' }}
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
  name: "StrongCaptchaModal",
  props: ["lang", "value"],
  data() {
    return {
      code: '',
      loaded: false,
      text: '',
      textValid: null,
      image: ''
    }
  },
  computed: {
    show: {
      get() {
        return this.value === 1;
      },
      set() {
        this.$emit('input', this.textValid ? 2 : null);
      }
    }
  },
  methods: {
    reset() {
      this.code = '';
      this.text = '';
      this.image = '';
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
            this.code = json.code;
            this.image = json.image;
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
              this.$bvModal.hide('strong-captcha');
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