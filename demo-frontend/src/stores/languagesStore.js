import { defineStore } from "pinia";

export const useLanguagesStore = defineStore({
  id: "languages",
  state: () => ({
    languages: [
        {
            'humanReadable': 'Java',
            'extension': 'java',
            'technical': 'java',
            'selectedAmount': 0
        },
        {
            'humanReadable': 'Python',
            'extension': 'py',
            'technical': 'python3',
            'selectedAmount': 0
        },
        {
            'humanReadable': 'Kotlin',
            'extension': 'kt',
            'technical': 'kt',
            'selectedAmount': 0
        }
    ],
  }),

  getters: {},

  actions: {},
});
