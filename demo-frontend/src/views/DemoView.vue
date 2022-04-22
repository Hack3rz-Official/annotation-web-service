<script setup>
import { ref, watch} from "vue";
import File from "../composables/fileClass";
import {
  getCommitsFromRepo,
  getFilesFromTree,
  sortTreeByLanguages,
} from "../composables/githubApiConnector";
import FileDetailModalVue from "../components/FileDetailModal.vue";
import { useFilesStore } from "../stores/filesStore";
import { useLanguagesStore } from "../stores/languagesStore";

const filesStore = useFilesStore();
const languagesStore = useLanguagesStore();

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

function fetchFilteredFiles(language, limit = 5) {
  let filtered = filesStore.filterFilesByLanguage(language).slice(0, limit);
  console.log(filtered);
  for (let path of filtered) {
    filesStore.files.push(new File(githubOwner.value, githubRepo.value, path));
  }
  for (let file of filesStore.files) {
    file.fetchRawCode();
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
  filesStore.languageFilesDict = sortTreeByLanguages(tree);
}

</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <!-- FileDetailModal -->
    <file-detail-modal-vue></file-detail-modal-vue>

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
          <button class="btn" @click="filesStore.loadTestFiles">load demo files</button>
        </div>

        <div v-show="Object.keys(filesStore.languageFilesDict).length > 0">
          The
          <span class="font-bold">{{ githubRepo }}</span> repository contains
          {{ filesStore.filterFilesByLanguage("java").length }} Java files,
          {{ filesStore.filterFilesByLanguage("py").length }} Python files and
          {{ filesStore.filterFilesByLanguage("kt").length }} Kotlin files.
          <ul class="mt-3 flex flex-col gap-2">
            <li v-for="language in languagesStore.languages" :key="language" class="flex flex-row gap-4 items-center">
              <input
                type="range"
                min="0"
                :max="filesStore.filterFilesByLanguage(language.extension).length"
                v-model="language.selectedAmount"
                class="range range-primary range-s w-64"
              />
              <button
                class="btn btn-primary mx-2"
                :class="{
                  'btn-disabled': filesStore.filterFilesByLanguage(language.extension).length == 0,
                }"
                @click="fetchFilteredFiles(language.extension, language.selectedAmount)"
              >
                Fetch {{ language.selectedAmount }} of
                {{ filesStore.filterFilesByLanguage(language.extension).length }} {{ language.humanReadable }} Files
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="my-4">
      <button class="btn btn-primary mx-2" @click="filesStore.highlightAllFiles">
        highlight all files
      </button>
      <button
        class="btn btn-outline btn-error mx-2"
        @click="filesStore.deleteAllFiles"
      >
        delete all files
      </button>
    </div>

    <div class="flex flex-wrap gap-3 relative">
      <div
        v-for="file in filesStore.files"
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
          @click="filesStore.setActiveFile(file)"
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

