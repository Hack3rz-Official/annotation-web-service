<script setup>
import { ref } from "vue";
import axios from "axios";

const inputCode = ref("public static void main(String[] args) {}");
const outputCode = ref("");
const languageOptions = ref(["java", "python3", "kotlin"]);
const selectedLanguage = ref("java");

function highlight() {
  let data = {
    code: inputCode.value,
    language: selectedLanguage.value,
  };
  axios.post("http://localhost:3000/highlight", data).then((response) => {
    // console.log(response.data);

    let outputElem = document.getElementById("code-output");
    outputElem.innerHTML = null;

    let newElement = document
      .createRange()
      .createContextualFragment(response.data);
    outputElem.appendChild(newElement);
  });
}
</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <!-- <h1 class="text-2xl py-4">Syntax Highlighting</h1> -->
    <p class="py-4">
      Highlight your Java, Python and Kotlin code with our Annotation Web
      Service. Highlight your Java, Python and Kotlin code with our Annotation
      Web Service. Highlight your Java, Python and Kotlin code with our
      Annotation Web Service.
    </p>
    <div class="flex flex-col gap-4 content-center w-full">
      <textarea
        id="code-input"
        name="code-input"
        rows="10"
        class="border-2 border-orange-400 p-2 w-full resize-none"
        v-model="inputCode"
      ></textarea>

      <div class="flex justify-center gap-2 w-min mx-auto">
        <select name="language-select" id="language-select" v-model="selectedLanguage">
          <option v-for="language in languageOptions" :key="language" :value="language">
            {{ language }}
          </option>
        </select>
        <p
          class="
            text-center
            w-min
            p-2
            mx-auto
            border-2 border-orange-500
            cursor-pointer
          "
          @click="highlight"
        >
          Highlight
        </p>
      </div>

      <div
        id="code-output"
        name="code-output"
        class="border-2 border-orange-400 p-2 w-full"
      ></div>
    </div>
  </main>
</template>
