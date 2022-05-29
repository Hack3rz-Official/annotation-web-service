import { defineStore } from "pinia";
import { useFilesStore } from './filesStore';

export const useSettingsStore = defineStore({
  id: "settings",
  state: () => ({
    maxRequests: 1, // how many concurrent requests are allowed for highlighting
    pendingRequests: 0, // amount of currently pending requests
    interval: 50, // ms before next request is tried
    performanceMode: false, // deactivate file cards to prevent performance slowdown
  }),

  getters: {},

  actions: {
    togglePerformanceMode() {
      this.performanceMode = !this.performanceMode;
      // side-effect: if toggled to true, we need to trigger render of all previews, otherwise they remain blank.
      setTimeout(() => {
        if (!this.performanceMode) {
          const filesStore = useFilesStore();
          for (let file of filesStore.files) {
            file.displayHighlightedCard();
          }
        }
      }, 10)
    },
  },
});
