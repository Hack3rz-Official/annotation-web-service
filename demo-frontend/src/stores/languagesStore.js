import { defineStore } from "pinia";

export const useLanguagesStore = defineStore({
  id: "languages",
  state: () => ({
    languages: [
      {
        humanReadable: "Java",
        extension: "java",
        technical: "java",
        selectedAmount: 0,
      },
      {
        humanReadable: "Python",
        extension: "py",
        technical: "python3",
        selectedAmount: 0,
      },
      {
        humanReadable: "Kotlin",
        extension: "kt",
        technical: "kotlin",
        selectedAmount: 0,
      },
    ],
  }),

  getters: {
    languagesExtendedWithGo: (state) => {
      return state.languages.concat([{
        'humanReadable': 'Go',
        'extension': 'go',
        'technical': 'go',
    }]);
    },
  },

  actions: {},
});
