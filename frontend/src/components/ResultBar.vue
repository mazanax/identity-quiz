<template>
  <b-progress :variant="chosen ? 'success' : 'primary'" height="50px" :value="value" :max="total" show-value class="mb-3"/>
</template>

<script>
export default {
  name: "ResultBar",
  props: ["value", "total", "chosen"]
}
</script>

<style scoped>

</style>