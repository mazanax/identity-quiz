<template>
  <div class="mt-5 text-center">
    <h5>{{ lang === 'ru' ? 'Поделиться с друзьями' : 'Share with friends' }}</h5>

    <a :href="`https://www.addtoany.com/add_to/facebook?linkurl=${url}%2F&amp;linkname=${name}`"
       target="_blank" class="d-inline-block p-1"><img
        src="https://static.addtoany.com/buttons/facebook.svg" class="share-icon"></a><!--
                    --><a
      :href="`https://www.addtoany.com/add_to/twitter?linkurl=${url}%2F&amp;linkname=${name}`"
      target="_blank" class="d-inline-block p-1"><img
      src="https://static.addtoany.com/buttons/twitter.svg" class="share-icon"></a><!--
                    --><a
      :href="`https://www.addtoany.com/add_to/vk?linkurl=${url}%2F&amp;linkname=${name}`"
      target="_blank" class="d-inline-block p-1"><img src="https://static.addtoany.com/buttons/vk.svg"
                                                      class="share-icon"></a><!--
                    --><a
      :href="`https://www.addtoany.com/add_to/odnoklassniki?linkurl=${url}%2F&amp;linkname=${name}`"
      target="_blank" class="d-inline-block p-1"><img
      src="https://static.addtoany.com/buttons/odnoklassniki.svg" class="share-icon"></a><!--
                    --><a
      :href="`https://www.addtoany.com/add_to/linkedin?linkurl=${url}%2F&amp;linkname=${name}`"
      target="_blank" class="d-inline-block p-1"><img
      src="https://static.addtoany.com/buttons/linkedin.svg" class="share-icon"></a><!--
                    --><a
      :href="`https://www.addtoany.com/add_to/whatsapp?linkurl=${url}%2F&amp;linkname=${name}`"
      target="_blank" class="d-inline-block p-1"><img
      src="https://static.addtoany.com/buttons/whatsapp.svg" class="share-icon"></a><!--
                    --><a
      :href="`https://www.addtoany.com/add_to/telegram?linkurl=${url}%2F&amp;linkname=${name}`"
      target="_blank" class="d-inline-block p-1"><img
      src="https://static.addtoany.com/buttons/telegram.svg" class="share-icon"></a><!--
                    --><a
      :href="`https://www.addtoany.com/add_to/email?linkurl=${url}%2F&amp;linkname=${name}`"
      target="_blank" class="d-inline-block p-1"><img
      src="https://static.addtoany.com/buttons/email.svg" class="share-icon"></a>
  </div>
</template>

<script>
export default {
  name: "Share",
  props: ["lang"],
  computed: {
    url() {
      return `${window.location.protocol}//${window.location.host}/`
    },
    name() {
      return this.lang === 'ru' ? 'Кто ты: человек или робот?' : 'Who are you: human or robot?'
    }
  }
}
</script>

<style scoped>

</style>