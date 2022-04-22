import { defineStore } from "pinia";

export const useFilesStore = defineStore({
  id: "files",
  state: () => ({
    files: [],
    activeFile: null,
  }),

  getters: {
    doubleCount: (state) => state.counter * 2,
  },

  actions: {
    deleteAllFiles() {
      this.files = [];
    },
    setActiveFile(file) {
      this.activeFile = file;
    },
  },
});
