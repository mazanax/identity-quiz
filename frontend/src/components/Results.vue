<template>
  <b-col sm="12" md="8" class="text-center">
    <h4>{{ lang === 'ru' ? 'Человек' : 'Human' }}</h4>
    <ResultBar v-if="loaded" :chosen="answer === 0" :value="humans" :total="total"/>
    <div v-else>
      <b-skeleton width="85%"></b-skeleton>
      <b-skeleton width="55%"></b-skeleton>
    </div>

    <h4>{{ lang === 'ru' ? 'Робот' : 'Robot' }}</h4>
    <ResultBar v-if="loaded" :chosen="answer === 1" :value="robots" :total="total"/>
    <div v-else>
      <b-skeleton width="85%"></b-skeleton>
      <b-skeleton width="55%"></b-skeleton>
    </div>

    <Share v-if="loaded" :lang="lang"/>
  </b-col>
</template>

<script>
import ResultBar from "@/components/ResultBar";
import Share from "@/components/Share";
import {api} from "@/api";

export default {
  name: "Results",
  components: {ResultBar, Share},
  props: ["lang"],
  mounted() {
    api.makeRequest("GET", "/stats")
        .then(response => response.json())
        .then(json => {
          this.answer = json.answer;
          this.humans = json.humans;
          this.robots = json.robots;
          this.loaded = true;
        })
  },
  data() {
    return {
      loaded: false,
      answer: 0,
      humans: 0,
      robots: 0,
    }
  },
  computed: {
    total() {
      return this.humans + this.robots
    }
  }
}
</script>

<style scoped>

</style>