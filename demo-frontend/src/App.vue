<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from '@/components/HelloWorld.vue'
</script>

<template>
  <header class="container mx-auto flex items-center justify-between py-5 px-3 bg-slate-300">
    <div>
      { Annotation Web Service }
    </div>
    <div class="">
      by Hack3rZ
    </div>
  </header>

  <RouterView />
</template>

<style>

</style>