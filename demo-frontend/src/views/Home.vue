<script setup>
import { ref } from "vue";
import FileDetailModalVue from "../components/FileDetailModal.vue";
import LoadRepoFiles from "../components/LoadRepoFiles.vue";
import LoadBenchmarkFilesVue from "../components/LoadBenchmarkFiles.vue";
import FilePreview from "../components/FilePreview.vue";
import FilePreviewCoverVue from "../components/FilePreviewCover.vue";
import Statistics from "../components/Statistics.vue";
import Settings from "../components/Settings.vue";
import { useFilesStore } from "../stores/filesStore";
import { useSettingsStore } from "../stores/settingsStore";
import { useLanguagesStore } from "../stores/languagesStore";

const filesStore = useFilesStore();
const settingsStore = useSettingsStore();
const languagesStore = useLanguagesStore();

const activeTab = ref("load-repo-files");

function setActiveTab(tabName) {
  activeTab.value = tabName;
}
</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <!-- FileDetailModal -->
    <file-detail-modal-vue></file-detail-modal-vue>

    <div class="tabs">
      <a
        class="tab tab-lifted"
        :class="{ '!bg-base-200 tab-active': activeTab == 'load-repo-files' }"
        @click="setActiveTab('load-repo-files')"
        >Load Repo Files</a
      >
      <a
        class="tab tab-lifted"
        :class="{
          '!bg-base-200 tab-active': activeTab == 'load-benchmark-files',
        }"
        @click="setActiveTab('load-benchmark-files')"
        >Load Benchmark Files</a
      >
      <a
        class="tab tab-lifted"
        :class="{ '!bg-base-200 tab-active': activeTab == 'statistics' }"
        @click="setActiveTab('statistics')"
        >Statistics</a
      >
      <a
        class="tab tab-lifted"
        :class="{ '!bg-base-200 tab-active': activeTab == 'settings' }"
        @click="setActiveTab('settings')"
        >Settings</a
      >
    </div>

    <div
      v-show="activeTab == 'load-repo-files'"
      class="card w-full bg-base-200 shadow-xl rounded-t-none"
    >
      <load-repo-files></load-repo-files>
    </div>
    <div
      v-show="activeTab == 'load-benchmark-files'"
      class="card w-full bg-base-200 shadow-xl rounded-t-none"
    >
      <load-benchmark-files-vue></load-benchmark-files-vue>
    </div>
    <div
      v-show="activeTab == 'statistics'"
      class="card w-full bg-base-200 shadow-xl rounded-t-none"
    >
      <statistics></statistics>
    </div>
    <div
      v-show="activeTab == 'settings'"
      class="card w-full bg-base-200 shadow-xl rounded-t-none"
    >
      <settings></settings>
    </div>

    <!-- Action Buttons -->
    <div class="my-4" v-if="filesStore.files.length > 0">
      <button
        class="btn btn-primary mx-2"
        @click="filesStore.highlightAllFiles"
      >
        highlight all files
      </button>
      <button
        class="btn btn-outline btn-error mx-2"
        @click="filesStore.deleteAllFiles"
      >
        delete all files
      </button>
    </div>

    <div v-else class="hero mt-10">
      <div class="hero-content flex-col lg:flex-row-reverse">
        <img
          src="@/assets/highlighting.png"
          class="max-w-sm rounded-lg"
        />
        <div>
          <h1 class="text-5xl font-bold">Annotation Web Service </h1>
          <h2 class="text-3xl font-bold opacity-70">Demo</h2>
          <p class="py-6">
            Welcome to the frontend of our Syntax Highlighting Service. 
            This Demo is intended to let you experience the capabilities of our service first-hand. You can load files from public Github repositories or use our benchmark files for testing.

          </p>
          <!-- <button class="btn btn-primary">Get Started</button> -->
        </div>
      </div>
    </div>

    <!-- File Previews for each loaded file -->
    <div
      style="min-height: 450px"
      class="flex gap-x-52"
      :class="{ 'flex-col': !settingsStore.performanceMode }"
    >
      <div
        v-for="language in languagesStore.languages"
        :key="language.technical"
        class="relative my-3"
        v-show="
          filesStore.filterFetchedFilesByLanguage(language.extension).length > 0
        "
      >
        <file-preview-cover-vue
          :language="language"
          :files="filesStore.filterFetchedFilesByLanguage(language.extension)"
        ></file-preview-cover-vue>
        <div
          v-if="!settingsStore.performanceMode"
          class="
            file-preview-container
            flex flex-row-reverse
            gap-3
            relative
            overflow-x-scroll
            w-min
            max-w-full
          "
        >
          <!-- eslint-disable-next-line vue/no-v-for-template-key -->
          <template
            v-for="file in filesStore.filterFetchedFilesByLanguage(
              language.extension
            )"
            :key="file.uuid"
          >
            <file-preview :file="file"></file-preview>
          </template>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped lang="scss">
.file-preview-container {
  padding-right: 100px;
}
</style>

