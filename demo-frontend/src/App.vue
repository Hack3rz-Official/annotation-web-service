<script setup>
import { RouterView } from "vue-router";
</script>

<template>
  <header class="container mx-auto">
    <div class="navbar mb-5">
      <a class="btn btn-ghost normal-case text-xl">
        <div class="text-3xl">
          <span class="">{ </span>
          <span class="text-primary text-4xl font-bold">A</span>nnotation
          <span class="text-primary text-4xl font-bold">W</span>eb
          <span class="text-primary text-4xl font-bold">S</span>ervice
          <span class="">}</span>
        </div>
      </a>
    </div>
  </header>

  <RouterView />
</template>

<style>
</style>