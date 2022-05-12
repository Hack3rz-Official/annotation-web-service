import { defineStore } from "pinia";

export const useSettingsStore = defineStore({
  id: "settings",
  state: () => ({
      maxRequests: 1, // how many concurrent requests are allowed for highlighting
      pendingRequests: 0, // amount of currently pending requests
      interval: 10, // ms before next request is tried
      performanceMode: false // deactivate file cards to prevent performance slowdown
  }),

  getters: {},

  actions: {
    togglePerformanceMode() {
      this.performanceMode = !this.performanceMode
    }
  },
});
