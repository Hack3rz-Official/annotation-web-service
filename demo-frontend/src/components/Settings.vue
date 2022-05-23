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

    <p class="mt-5">
      Performance Mode (activate if you load many files to prevent performance issues):
      <!-- <span class="font-bold">{{ settingsStore.performanceMode ? 'ON' : 'OFF' }}</span> -->
    </p>
    <div class="form-control">
      <div class="input-group">
        <button
          class="btn btn- w-1/2"
          :class="{ 'btn-outline': !settingsStore.performanceMode }"
          @click="settingsStore.togglePerformanceMode"
        >
          On
        </button>
        <button
          class="btn btn- w-1/2"
          :class="{ 'btn-outline': settingsStore.performanceMode }"
          @click="settingsStore.togglePerformanceMode"
        >
          Off
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
</style>
