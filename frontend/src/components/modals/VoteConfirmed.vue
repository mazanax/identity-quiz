<template>
  <b-modal
      v-model="show"
      id="vote-confirmed"
      hide-footer
      :title="lang === 'ru' ? 'Ответ засчитан!' : 'Answer has been saved!'">
    <div class="display-1 text-center">
      <b-icon-check-circle class="text-success"/>

      <b-btn block size="lg" variant="outline-primary" class="mt-5" @click="handleOk()"
        >{{ lang === 'ru' ? 'Посмотреть результаты' : 'Show Results' }}</b-btn>
    </div>
  </b-modal>
</template>

<script>
export default {
  name: "VoteConfirmed",
  props: ["lang", "value"],
  computed: {
    show: {
      get() {
        return this.value === 3;
      },
      set() {
        this.$emit('input', null);
      }
    }
  },
  methods: {
    handleOk() {
      window.location.reload();
    }
  }
}
</script>

<style scoped>

</style>