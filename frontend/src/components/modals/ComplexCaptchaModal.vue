<template>
  <b-modal
      v-model="show"
      id="complex-captcha"
      :title="lang === 'ru' ? 'Подтвердите, что вы не робот' : 'Confirm that you are not robot'"
      @ok="handleOk"
      :ok-disabled="!text.length || !loaded"
      :cancel-title="lang === 'ru' ? 'Отмена' : 'Cancel'"
      @show="reset">
    <div v-if="lang === 'ru'">
      <b-card bg-variant="light">Отлично. Мы все больше склоняемся к тому, что вы человек. <!--
      -->Однако некоторые хитрые роботы могут распознать текст с картинки, а значит вы можете быть одним из них.
      </b-card>
      <div v-if="loaded" class="my-4 text-center">Выберите все квадраты, на которых изображены <b>{{ question }}</b>.</div>
    </div>
    <div v-else>
      <b-card bg-variant="light">Great. We're more and more inclined to think that you are human. <!--
      -->However, some tricky robots can recognize text from a picture, which means you might be one of them.
      </b-card>

      <div v-if="loaded" class="my-4 text-center">Please choose all the squares where <b>{{ question }}</b> are displayed.</div>
    </div>

    <form method="post" @submit="handleOk">
      <b-row cols="3">
        <b-col :key="`complex-captcha-${img}`" v-for="img of images.keys()">
          <div class="mx-2 my-2 w-100 img-wrapper">
            <div v-if="selected.indexOf(img) !== -1" class="img-checked"><b-icon-check/></div>
            <b-img fluid-grow :src="`data:image/jpeg;base64,${images[img]}`" class="cursor-pointer" @click="toggleImage(img)"/>
          </div>
        </b-col>
      </b-row>

      <div v-if="false === textValid" class="text-danger">
        {{ lang === 'ru' ? 'Неправильный ответ' : 'Invalid answer' }}
      </div>
    </form>
  </b-modal>
</template>

<script>
import {api} from "@/api";

export default {
  name: "ComplexCaptchaModal",
  props: ["lang", "value"],
  data() {
    return {
      loaded: false,
      images: [],
      selected: [],
      textValid: null,
      questionRaw: 'cats'
    }
  },
  computed: {
    text() {
      return this.selected.join("");
    },
    show: {
      get() {
        return this.value === 2;
      },
      set() {
        this.$emit('input', this.textValid ? 3 : null);
      }
    },
    question() {
      switch (this.questionRaw) {
        case 'cars':
          return this.lang === 'ru' ? 'автомобили' : 'cars';
        case 'cats':
          return this.lang === 'ru' ? 'кошки' : 'cats';
        case 'dogs':
          return this.lang === 'ru' ? 'собаки' : 'dogs';
        case 'fish':
          return this.lang === 'ru' ? 'рыбы' : 'fish';
        case 'planes':
          return this.lang === 'ru' ? 'самолеты' : 'planes';
        case 'trees':
          return this.lang === 'ru' ? 'деревья' : 'trees';
      }

      return '';
    }
  },
  methods: {
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
              this.$bvModal.hide('complex-captcha');
            }, 400);
          })
          .catch((err) => {
            console.error(err);
            this.reset();
            this.textValid = false;
          });
    },
    reset() {
      this.textValid = null;
      this.loaded = false;
      this.selected = [];

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
            this.questionRaw = json.question;
            this.code = json.code;
            this.images = json.images;
            this.loaded = true;
          });
    },
    toggleImage(idx) {
      if (this.selected.indexOf(idx) === -1) {
        this.selected.push(idx);
      } else {
        this.selected = this.selected.filter(v => v !== idx);
      }
      console.log(this.selected.sort());
    }
  }
}
</script>

<style scoped>

</style>