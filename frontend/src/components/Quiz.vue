<template>
  <b-col sm="12" md="8">
    <b-btn size="lg" block variant="outline-primary"
           :disabled="!auth" @click="sendAnswer(0)">{{ lang === 'ru' ? 'Человек' : 'Human' }}</b-btn>
    <b-btn size="lg" block variant="outline-primary"
           :disabled="!auth" @click="sendAnswer(1)">{{ lang === 'ru' ? 'Робот' : 'Robot' }}</b-btn>

    <SimpleCaptchaModal :lang="lang" v-model="step"/>
    <StrongCaptchaModal :lang="lang" v-model="step"/>
    <ComplexCaptchaModal :lang="lang" v-model="step"/>
    <VoteConfirmed :lang="lang" v-model="step"/>
  </b-col>
</template>

<script>
import SimpleCaptchaModal from "@/components/modals/SimpleCaptchaModal";
import StrongCaptchaModal from "@/components/modals/StrongCaptchaModal";
import VoteConfirmed from "@/components/modals/VoteConfirmed";
import ComplexCaptchaModal from "@/components/modals/ComplexCaptchaModal";
import {api} from "@/api";

export default {
  name: "Quiz",
  components: {SimpleCaptchaModal, StrongCaptchaModal, ComplexCaptchaModal, VoteConfirmed},
  props: ["auth", "lang"],
  computed: {
    step: {
      get() {
        return this.$store.state.step;
      },
      set(step) {
        this.$store.commit('setStep', step);
      }
    }
  },
  methods: {
    sendAnswer(option) {
      if (option !== 0 && option !== 1) {
        console.error(`Unknown option: ${option}`);
        return;
      }

      api.makeRequest('POST', '/answer', {'body': JSON.stringify({'option': option})})
        .then(() => {
          this.step = 3;
        })
        .catch((response) => {
          if (response.status === 418) {
            response.json().then(json => {
              this.step = json.step || 0;
            })
          } else {
            console.error(response);

            const errMessage = this.lang === 'ru'
                ? 'Произошла ошибка при отправке ответа'
                : 'There was an error when requesting the answer';

            this.$bvToast.toast(errMessage, {
              noCloseButton: true,
              autoHideDelay: 2000,
              variant: 'danger',
              solid: true,
            });

            setTimeout(() => {
              location.reload();
            }, 2000);
          }
        })
    }
  }
}
</script>

<style scoped>

</style>