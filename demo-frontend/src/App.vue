<script setup>
import { RouterLink, RouterView } from "vue-router";
import HelloWorld from "@/components/HelloWorld.vue";
</script>

<template>
  <header class="container mx-auto flex items-center justify-between py-5 px-3">
    <div class="text-3xl">
      <span class="text-gray-400">{</span>
      <span class="text-red-600 text-4xl font-bold">A</span>nnotation
      <span class="text-red-600 text-4xl font-bold">W</span>eb
      <span class="text-red-600 text-4xl font-bold">S</span>ervice
      <span class="text-gray-400">}</span>
      <span class="text-gray-400"> - </span>
      <span class="text-black italic"> Demo </span>
    </div>
    <div class="">by Hack3rZ</div>
  </header>

  <RouterView />
</template>

<style>
</style>