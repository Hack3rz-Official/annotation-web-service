<script setup>
import { onMounted, ref, watch, computed } from "vue";
import axios from "axios";
import File from "../composables/fileClass";
import { useFileFixtures } from "../composables/useFileFixtures";
import {
  getCommitsFromRepo,
  getFilesFromTree,
  sortTreeByLanguages,
} from "../composables/githubApiConnector";
import FileDetailModalVue from "../components/FileDetailModal.vue";

const githubRepoUrl = ref(
  "https://github.com/Hack3rz-Official/annotation-web-service"
);
const githubOwner = ref("Hack3rz-Official");
const githubRepo = ref("annotation-web-service");

watch(githubRepoUrl, (newRepoUrl, oldRepoUrl) => {
  let splitted = newRepoUrl.split("/");
  githubOwner.value = splitted[3];
  githubRepo.value = splitted[4];
});

const highlightedCode = ref(``);

const files = ref([]);
const activeFile = ref(null);

const languageFilesDict = ref({});
const amountJavaFiles = ref(0);
const amountPythonFiles = ref(0);
const amountKotlinFiles = ref(0);

function loadTestFiles() {
  files.value = useFileFixtures();
  for (let file of files.value) {
    file.fetchRawCode()
  }
}

function highlightAllFiles() {
  for (let file of files.value) {
    if (file.status != "highlighted") {
      file.highlight();
    }
  }
}

function deleteAllFiles() {
  files.value = [];
}

function setActiveFile(file) {
  activeFile.value = file;
}

function closeFileModal() {
  activeFile.value = null;
}

function fetchFilteredFiles(language, limit = 5) {
  let filtered = filterFilesByLanguage(language).slice(0, limit);
  console.log(filtered);
  for (let path of filtered) {
    files.value.push(new File(githubOwner.value, githubRepo.value, path));
  }
  for (let file of files.value) {
    file.fetchRawCode()
  }
}

async function loadFilesFromRepo() {
  const tree_sha = await getCommitsFromRepo(
    githubOwner.value,
    githubRepo.value
  );
  const tree = await getFilesFromTree(
    githubOwner.value,
    githubRepo.value,
    tree_sha
  );
  languageFilesDict.value = sortTreeByLanguages(tree);
  console.log(languageFilesDict.value);
}

function filterFilesByLanguage(language) {
  if (!languageFilesDict.value || !(language in languageFilesDict.value)) {
    return [];
  } else {
    return languageFilesDict.value[language];
  }
}
</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <!-- FileDetailModal -->
    <file-detail-modal-vue
      :activeFile="activeFile"
      @close-file-modal="closeFileModal"
    ></file-detail-modal-vue>

    <div class="card w-full bg-base-200 mt-3 shadow-xl">
      <div class="card-body">
        <div
          class="form-control flex flex-row justify-start items-center gap-4"
        >
          <div class="input-group w-auto grow">
            <input
              type="text"
              placeholder="https://github.com/{owner}/{repo}"
              v-model="githubRepoUrl"
              class="input input-bordered w-full"
            />
            <button class="btn" @click="loadFilesFromRepo()">
              Load Files from Repo
            </button>
          </div>
          or
          <button class="btn" @click="loadTestFiles">load test files</button>
        </div>

        <div v-show="Object.keys(languageFilesDict).length > 0">
          The
          <span class="font-bold">{{ githubRepo }}</span> repository contains
          {{ filterFilesByLanguage("java").length }} Java files,
          {{ filterFilesByLanguage("py").length }} Python files and
          {{ filterFilesByLanguage("kt").length }} Kotlin files.
          <ul class="mt-3 flex flex-col gap-2">
            <li class="flex flex-row gap-4 items-center">
              <input
                type="range"
                min="0"
                :max="filterFilesByLanguage('java').length"
                v-model="amountJavaFiles"
                class="range range-primary range-s w-64"
              />
              <button
                class="btn btn-primary mx-2"
                :class="{
                  'btn-disabled': filterFilesByLanguage('java').length == 0,
                }"
                @click="fetchFilteredFiles('java', amountJavaFiles)"
              >
                Fetch {{ amountJavaFiles }} of
                {{ filterFilesByLanguage("java").length }} Java Files
              </button>
            </li>
            <li class="flex flex-row gap-4 items-center">
              <input
                type="range"
                min="0"
                :max="filterFilesByLanguage('py').length"
                v-model="amountPythonFiles"
                class="range range-primary range-s w-64"
              />
              <button
                class="btn btn-primary mx-2"
                :class="{
                  'btn-disabled': filterFilesByLanguage('py').length == 0,
                }"
                @click="fetchFilteredFiles('py', amountPythonFiles)"
              >
                Fetch {{ amountPythonFiles }} of
                {{ filterFilesByLanguage("py").length }} Python Files
              </button>
            </li>
            <li class="flex flex-row gap-4 items-center">
              <input
                type="range"
                min="0"
                :max="filterFilesByLanguage('kt').length"
                v-model="amountKotlinFiles"
                class="range range-primary range-s w-64"
              />
              <button
                class="btn btn-primary mx-2"
                :class="{
                  'btn-disabled': filterFilesByLanguage('kt').length == 0,
                }"
                @click="fetchFilteredFiles('kt', amountKotlinFiles)"
              >
                Fetch {{ amountKotlinFiles }} of
                {{ filterFilesByLanguage("kt").length }} Kotlin Files
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="my-4">
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
            @click.stop="file.highlight()"
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

