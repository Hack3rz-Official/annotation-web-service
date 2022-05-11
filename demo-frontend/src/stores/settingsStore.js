import { defineStore } from "pinia";

export const useSettingsStore = defineStore({
  id: "settings",
  state: () => ({
      maxRequests: 4, // how many concurrent requests are allowed for highlighting
      pendingRequests: 0, // amount of currently pending requests
      interval: 10, // ms before next request is tried
  }),

  getters: {},

  actions: {},
});
