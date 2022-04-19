<script setup>
import { onMounted, ref, watch, computed } from "vue";
import axios from "axios";

const isLoading = ref(false);
// const githubUser = ref("pallets");
// const githubRepo = ref("flask");
// const githubFile = ref("src/flask/views.py");
const githubUser = ref("elastic");
const githubRepo = ref("elasticsearch");
const githubFile = ref("build-tools/src/main/java/org/elasticsearch/gradle/util/Pair.java");
const rawCode = ref("");
const highlightedCode = ref(``);

const jsdelivrUrl = computed(() => {
  return `https://cdn.jsdelivr.net/gh/${githubUser.value}/${githubRepo.value}/${githubFile.value}`;
});

function fetchFile() {
  isLoading.value = true;
  axios
    .get(jsdelivrUrl.value)
    .then((response) => {
      console.log(response);
      rawCode.value = response.data;
      isLoading.value = false;
    })
    .catch((error) => {
      console.log(error);
      isLoading.value = false;
    });
}

function highlight() {
  isLoading.value = true;
  let data = {
    code: rawCode.value,
    language: "java",
  };
  let outputElem = document.getElementById("highlighted-code");
  axios
    .post("http://localhost:3000/highlight", data)
    .then((response) => {
      let newElement = document
        .createRange()
        .createContextualFragment(response.data);
      outputElem.innerHTML = null;
      outputElem.appendChild(newElement);
      highlightedCode.value = response.data;
      isLoading.value = false;
    })
    .catch((error) => {
      console.log(error);
      outputElem.innerHTML = "Error in Highlighting Service";
      isLoading.value = false;
    });
}
</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <div class="github-source-form form-control flex-row gap-2">
      <label class="github-user-input input-group input-group-vertical">
        <span>Github User</span>
        <input
          type="text"
          placeholder="Hack3rz-Official"
          v-model="githubUser"
          class="input input-bordered"
        />
      </label>
      <label class="github-repo-input input-group input-group-vertical">
        <span>Repository</span>
        <input
          type="text"
          placeholder="annotation-web-service"
          v-model="githubRepo"
          class="input input-bordered"
        />
      </label>
      <label class="github-file-input input-group input-group-vertical">
        <span>File</span>
        <input
          type="text"
          placeholder="src/main/java/com/hack3rz/annotationservice/controller/AnnotationController.java"
          v-model="githubFile"
          class="input input-bordered"
        />
      </label>
    </div>

    <div class="my-4">
      {{ jsdelivrUrl }}

      <button class="btn mx-2" @click="fetchFile">fetch file</button>
      <button class="btn" @click="highlight">Highlight</button>
    </div>

    <div class="flex gap-4">
      <div class="card w-full bg-base-200 shadow-md">
        <div class="card-body p-5">
          <textarea
            id="raw-code"
            wrap="off"
            class="resize-none font-mono text-sm bg-transparent"
            v-model="rawCode"
            disabled
          ></textarea>
        </div>
      </div>
      <div class="card w-full bg-base-200 shadow-md">
        <div class="card-body p-5">
          <div
            id="highlighted-code"
            wrap="off"
            class="resize-none font-mono text-sm bg-transparent overflow-auto"
            disabled
          ></div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped lang="scss">
.github-source-form {
  label {
    width: min-content;
  }
  .github-user-input {
    flex-grow: 1;
  }
  .github-repo-input {
    flex-grow: 1;
  }
  .github-file-input {
    flex-grow: 3;
  }
}

#raw-code,
#highlighted-code {
  height: 600px;
}
</style>

