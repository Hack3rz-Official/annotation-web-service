import { defineStore } from "pinia";
import { useFileFixtures } from "../composables/useFileFixtures";


export const useFilesStore = defineStore({
  id: "files",
  state: () => ({
    files: [],
    activeFile: null,
    languageFilesDict: {}
  }),

  getters: {},

  actions: {
    deleteAllFiles() {
      this.files = [];
    },
    setActiveFile(file) {
      this.activeFile = file;
    },
    loadTestFiles() {
      this.files = useFileFixtures();
      for (let file of this.files) {
        file.fetchRawCode();
      }
    },
    highlightAllFiles() {
      for (let file of this.files) {
        if (file.status != "highlighted") {
          file.highlight();
        }
      }
    },
    filterFilesByLanguage(language) {
      if (!this.languageFilesDict || !(language in this.languageFilesDict)) {
        return [];
      } else {
        return this.languageFilesDict[language];
      }
    }
  },
});
