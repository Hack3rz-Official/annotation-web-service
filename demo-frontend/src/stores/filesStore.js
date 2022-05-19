import { defineStore } from "pinia";
import { useFileFixtures } from "../composables/useFileFixtures";


export const useFilesStore = defineStore({
  id: "files",
  state: () => ({
    files: [],
    activeFile: null,
    languageFilesDict: {}
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
    loadTestFiles() {
      const fixtureFiles = useFileFixtures();
      for (let file of fixtureFiles) {
        this.files.push(file)
      }
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
    highlightSelectedFiles(files) {
      for (let file of files) {
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
    },
    filterFetchedFilesByLanguage(language) {
      return this.files.filter((file) => { return file.languageShort == language })
    }
  },
});
