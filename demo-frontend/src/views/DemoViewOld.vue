<script setup>
import { onMounted, ref, watch } from "vue";
import axios from "axios";
import { useRandomCode } from "../composables/useRandomCode";

const inputCode = ref("public static void main(String[] args) {}");
const languageOptions = ref(["java", "python3", "kotlin"]);
const selectedLanguage = ref("java");
const isLoading = ref(false);

watch(selectedLanguage, async (newSelectedLanguage, oldSelectedLanguage) => {
  if (newSelectedLanguage == oldSelectedLanguage) {
    return;
  }
  loadRandomCode();
});

watch(inputCode, async (newInputCode, oldInputCode) => {
  if (isLoading.value) {
    return;
  }
  highlight();
});

function highlight() {
  isLoading.value = true;
  let data = {
    code: inputCode.value,
    language: selectedLanguage.value,
  };
  let outputElem = document.getElementById("code-output");
  axios
    .post("http://localhost:3000/highlight", data)
    .then((response) => {
      let newElement = document
        .createRange()
        .createContextualFragment(response.data);
      outputElem.innerHTML = null;
      outputElem.appendChild(newElement);
      isLoading.value = false;
    })
    .catch((error) => {
      console.log(error);
      outputElem.innerHTML = "Error in Highlighting Service";
      isLoading.value = false;
    });
}

onMounted(() => {
  loadRandomCode();

  document
    .getElementById("code-input")
    .addEventListener("keydown", function (e) {
      if (e.key == "Tab") {
        e.preventDefault();
        var start = this.selectionStart;
        var end = this.selectionEnd;
        // set textarea value to: text before caret + tab + text after caret
        this.value =
          this.value.substring(0, start) + "\t" + this.value.substring(end);
        // put caret at right position again
        this.selectionStart = this.selectionEnd = start + 1;
      }
    });
    
  let codeOutputElement = document.getElementById("code-output");
  let codeInputElement = document.getElementById("code-input");
  codeInputElement.addEventListener("scroll", () => {
    codeOutputElement.scrollLeft = codeInputElement.scrollLeft;
    codeOutputElement.scrollTop = codeInputElement.scrollTop;
    // NOTE: the synching of the scroll is not always precise and may lag one letter behind
    // console.log(codeInputElement.scrollLeft + '<->' + codeOutputElement.scrollLeft);
  });
});

function loadRandomCode() {
  let randomCode = useRandomCode(selectedLanguage.value);
  inputCode.value = randomCode;
  highlight();
}
</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <p class="py-6 text-xl">
      Frontend Demo for the Annotation Web Service enabling realtime syntax
      highlighting. <br />
      Supported languages are Java, Python3 and Kotlin.
    </p>

    <div class="w-full flex flex-wrap justify-start gap-4 mb-4">
      <label for="language-select">Language:</label>
      <select
        name="language-select"
        id="language-select"
        class="p-2 bg-cyan-800 text-white hover:bg-cyan-600 hover:text-white"
        v-model="selectedLanguage"
      >
        <option
          v-for="language in languageOptions"
          :key="language"
          :value="language"
        >
          {{ language }}
        </option>
      </select>
    </div>

    <div class="code-wrapper relative">
      <textarea
        id="code-input"
        name="code-input"
        wrap="off"
        class="
          border-2 border-cyan-800
          p-2
          resize-none
          font-mono
          hide-text-show-caret
          absolute
        "
        v-model="inputCode"
      ></textarea>

      <div
        id="code-output"
        name="code-output"
        class="
          border-2 border-cyan-800
          p-2
          absolute
          pointer-events-none
          overflow-x-scroll
        "
      ></div>
    </div>
  </main>
</template>

<style lang="scss">
.hide-text-show-caret {
  color: black; /* sets the color of both caret and text */
  -webkit-text-fill-color: transparent; /* sets just the text color */
}

#code-input,
#code-output {
  width: 100%;
  height: 600px;
}
#code-input {
  z-index: 0;
}
#code-output {
  z-index: 1;
}
</style>

