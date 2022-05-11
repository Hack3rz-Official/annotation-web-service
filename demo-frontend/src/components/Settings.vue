<script setup>
import { ref } from "vue";
import { useSettingsStore } from "../stores/settingsStore";

const settingsStore = useSettingsStore();

const maxValue = ref(10);
</script>

<template>
  <div class="card-body">
    <p class="">
      maximum number of concurrent requests:
      <span class="font-bold">{{ settingsStore.maxRequests }}</span>
    </p>

    <input
      type="range"
      min="1"
      :max="maxValue"
      class="range"
      step="1"
      v-model="settingsStore.maxRequests"
    />
    <div class="w-full flex justify-between text-xs px-2">
      <span v-for="val of maxValue" :key="val" class="text-center ml-2">
        {{ val }}</span
      >
    </div>
  </div>
</template>

<style scoped lang="scss">
</style>
