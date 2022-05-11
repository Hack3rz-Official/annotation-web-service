<script setup>
import { ref, watch } from "vue";
import File from "../composables/fileClass";
import {
  getCommitsFromRepo,
  getFilesFromTree,
  sortTreeByLanguages,
} from "../composables/githubApiConnector";

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

// make sure the user can not enter an amount higher than the amount of available files
function selectedAmountChanged(extension) {
  let language = languagesStore.languages.find((elem) => {
    return elem.extension == extension;
  });
  let availableFiles = filesStore.filterFilesByLanguage(
    language.extension
  ).length;
  if (language.selectedAmount > availableFiles) {
    language.selectedAmount = availableFiles;
  }
}

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

  // set the selectedAmount to the maximum after loading files
  for (let language of languagesStore.languages) {
    language.selectedAmount = filesStore.filterFilesByLanguage(
      language.extension
    ).length;
  }
}
</script>

<template>
  <div class="card w-full bg-base-200 mt-3 shadow-xl">
    <div class="card-body">
      <div class="form-control flex flex-row justify-start items-center gap-4">
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
        <button class="btn" @click="filesStore.loadTestFiles">
          load demo files
        </button>
      </div>

      <div v-show="Object.keys(filesStore.languageFilesDict).length > 0">
        The
        <span class="font-bold">{{ githubRepo }}</span> repository contains
        {{ filesStore.filterFilesByLanguage("java").length }} Java files,
        {{ filesStore.filterFilesByLanguage("py").length }} Python files and
        {{ filesStore.filterFilesByLanguage("kt").length }} Kotlin files.
        <ul class="mt-3 flex flex-col gap-2">
          <li
            v-for="language in languagesStore.languages"
            :key="language"
            class="flex flex-row gap-4 items-center"
          >
            <input
              type="number"
              placeholder="# files"
              class="input w-24 max-w-xs"
              min="0"
              :max="filesStore.filterFilesByLanguage(language.extension).length"
              v-model="language.selectedAmount"
              @change="selectedAmountChanged(language.extension)"
              @keyup="selectedAmountChanged(language.extension)"
              :class="{
                'btn-disabled':
                  filesStore.filterFilesByLanguage(language.extension).length ==
                  0,
              }"
            />
            <!-- <input
              type="range"
              min="0"
              :max="filesStore.filterFilesByLanguage(language.extension).length"
              v-model="language.selectedAmount"
              class="range range-primary range-s w-64"
            /> -->
            <button
              class="btn btn-primary mx-2"
              :class="{
                'btn-disabled':
                  filesStore.filterFilesByLanguage(language.extension).length ==
                  0,
              }"
              @click="
                fetchFilteredFiles(language.extension, language.selectedAmount)
              "
            >
              <template
                v-if="
                  language.selectedAmount >=
                  filesStore.filterFilesByLanguage(language.extension).length
                "
              >
                Fetch all {{ language.selectedAmount }}
                {{ language.humanReadable }} Files
              </template>
              <template v-else>
                Fetch {{ language.selectedAmount }} of
                {{
                  filesStore.filterFilesByLanguage(language.extension).length
                }}
                {{ language.humanReadable }} Files
              </template>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
</style>
