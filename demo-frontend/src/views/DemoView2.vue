<script setup>
import { onMounted, ref, watch, computed } from "vue";
import axios from "axios";
import File from "../composables/fileClass";
import { useFileFixtures } from "../composables/useFileFixtures";
import FileDetailModalVue from "../components/FileDetailModal.vue";

const githubUser = ref("elastic");
const githubRepo = ref("elasticsearch");
const githubFile = ref(
  "server/src/main/java/org/elasticsearch/action/index/IndexAction.java"
);
const highlightedCode = ref(``);

const files = ref([]);
const activeFile = ref(null);

const showRaw = computed(() => {
  return highlightedCode.value == "";
});

function loadTestFiles() {
  files.value = useFileFixtures();
  for (let file of files.value) {
    fetchRawCode(file);
  }
}

function highlightAllFiles() {
  for (let file of files.value) {
    if (file.status != "highlighted") {
      highlight(file);
    }
  }
}

function deleteAllFiles() {
  files.value = [];
}

function setActiveFile(file) {
  console.log("setActiveModal", file);
  activeFile.value = file;
}

function closeFileModal() {
  console.log("closeFileModal");
  activeFile.value = null;
}

function fetchRawCode(file) {
  axios
    .get(`${File.jsDelivrBaseUrl}${file.identifier}`)
    .then((response) => {
      // console.log(response);
      file.rawCode = response.data;
      file.size = response.data.length;
      file.status = "raw";
    })
    .catch((error) => {
      console.log(error);
      file.status = "empty";
    });
}

function highlight(file) {
  //   console.log("requested highlighting for file", file);
  file.status = "loading";
  file.request.startTimestamp = Date.now();
  let data = {
    code: file.rawCode,
    language: file.languageLong,
  };
  let outputElem = document.getElementById(file.identifier);
  //   console.log(outputElem);
  axios
    .post("http://localhost:3000/highlight", data)
    .then((response) => {
      let newElement = document
        .createRange()
        .createContextualFragment(response.data);
      outputElem.innerHTML = null;
      outputElem.appendChild(newElement);
      //   console.log(newElement);
      //   console.log(outputElem);
      file.highlightedCode = response.data;
      file.status = "highlighted";
      file.request.endTimestamp = Date.now();
      file.request.duration =
        file.request.endTimestamp - file.request.startTimestamp;
    })
    .catch((error) => {
      console.log(error);
      outputElem.innerHTML = "Error in Highlighting Service";
      file.status = "failed";
      file.request.endTimestamp = Date.now();
      file.request.duration =
        file.request.endTimestamp - file.request.startTimestamp;
    });
}
</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <!-- FileDetailModal -->
    <file-detail-modal-vue
      :activeFile="activeFile"
      @close-file-modal="closeFileModal"
      @highlight-file="highlight(activeFile)"
    ></file-detail-modal-vue>

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
      <button class="btn btn-primary mx-2" @click="loadTestFiles">
        load test files
      </button>
      <button class="btn btn-primary mx-2" @click="highlightAllFiles">
        highlight all files
      </button>
      <button class="btn btn-outline btn-error mx-2" @click="deleteAllFiles">
        delete all files
      </button>
    </div>

    <div class="flex flex-wrap gap-3 relative">
      <div
        v-for="file in files"
        :key="file.identifier"
        class="
          file-wrapper
          card card-compact
          w-full
          bg-base-200
          shadow-md
          border-2
        "
      >
        <!-- overlay div for hover and click effect -->
        <div
          class="
            absolute
            h-full
            w-full
            flex
            justify-center
            content-center
            cursor-pointer
            opacity-0
            hover:opacity-100 hover:bg-black/20
          "
          @click="setActiveFile(file)"
        >
          <!-- button -->
          <button
            class="btn btn-primary m-auto"
            :class="{ 'btn-disabled': file.status == 'highlighted' }"
            @click.stop="highlight(file)"
          >
            Highlight
          </button>
        </div>
        <!-- this card-body is shown when there is only raw code -->
        <div class="card-body mt-3" v-show="!file.highlightedCode">
          <textarea
            id="raw-code"
            wrap="off"
            class="
              resize-none
              font-mono
              text-sm
              bg-transparent
              overflow-hidden
              text-tiny
            "
            v-model="file.rawCode"
            disabled
          ></textarea>
        </div>
        <!-- this card-body is shown when code has been highlighted -->
        <div class="card-body mt-3" v-show="file.highlightedCode">
          <div
            :id="file.identifier"
            wrap="off"
            class="
              resize-none
              font-mono
              text-sm
              bg-transparent
              overflow-hidden
              text-tiny
            "
            disabled
          ></div>
        </div>
        <!-- file name badge -->
        <div
          class="badge w-full h-6 absolute rounded-none"
          :class="{
            'badge-success': file.status == 'highlighted',
            'badge-warning': file.status == 'loading',
            'badge-error': file.status == 'failed',
          }"
        >
          {{ file.getFilenameShortened() }}.<span class="font-bold">{{
            file.languageShort
          }}</span>
        </div>
        <!-- file size and request status information -->
        <div
          class="absolute w-full h-8 rounded rounded-t-none border-0 bottom-0"
        >
          <div class="badge absolute m-2 right-0">
            {{ file.request.duration }} ms
          </div>
          <div class="badge absolute m-2 left-0">
            {{ file.getSizeFormatted() }}
          </div>
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

.file-wrapper {
  height: 400px;
  width: 290px;
  .card-body {
    height: calc(100% - 50px);
    div,
    textarea {
      height: 100%;
    }
  }
}

.text-tiny {
  font-size: 6px;
  line-height: 6px;
}
</style>

