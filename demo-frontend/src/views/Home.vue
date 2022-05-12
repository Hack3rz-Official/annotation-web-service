<script setup>
import { ref } from "vue";
import FileDetailModalVue from "../components/FileDetailModal.vue";
import LoadRepoFiles from "../components/LoadRepoFiles.vue";
import LoadBenchmarkFilesVue from "../components/LoadBenchmarkFiles.vue";
import FilePreview from "../components/FilePreview.vue";
import Statistics from "../components/Statistics.vue"
import Settings from "../components/Settings.vue"
import { useFilesStore } from "../stores/filesStore";
import { useSettingsStore } from "../stores/settingsStore";

const filesStore = useFilesStore();
const settingsStore = useSettingsStore();

const activeTab = ref("load-repo-files");

function setActiveTab(tabName) {
  activeTab.value = tabName;
}
</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <!-- FileDetailModal -->
    <file-detail-modal-vue v-if="!settingsStore.performanceMode"></file-detail-modal-vue>

    <div class="tabs">
      <a
        class="tab tab-lifted"
        :class="{ '!bg-base-200 tab-active': activeTab == 'load-repo-files' }"
        @click="setActiveTab('load-repo-files')"
        >Load Repo Files</a
      >
      <a
        class="tab tab-lifted"
        :class="{ '!bg-base-200 tab-active': activeTab == 'load-benchmark-files' }"
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
    <div class="my-4">
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

    <!-- File Previews for each loaded file -->
    <div v-if="!settingsStore.performanceMode" class="flex flex-wrap gap-3 relative">
      <!-- eslint-disable-next-line vue/no-v-for-template-key -->
      <template v-for="file in filesStore.files" :key="file.uuid">
        <file-preview :file="file"></file-preview>
      </template>
    </div>
  </main>
</template>

<style scoped lang="scss">
</style>

