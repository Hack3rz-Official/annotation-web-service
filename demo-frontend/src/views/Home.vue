<script setup>
import { ref } from "vue";
import FileDetailModalVue from "../components/FileDetailModal.vue";
import LoadFiles from "../components/LoadFiles.vue";
import FilePreview from "../components/FilePreview.vue";
import Statistics from "../components/Statistics.vue"
import { useFilesStore } from "../stores/filesStore";

const filesStore = useFilesStore();

const activeTab = ref("load-files");

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
        :class="{ '!bg-base-200 tab-active': activeTab == 'load-files' }"
        @click="setActiveTab('load-files')"
        >Load Files</a
      >
      <a
        class="tab tab-lifted"
        :class="{ '!bg-base-200 tab-active': activeTab == 'statistics' }"
        @click="setActiveTab('statistics')"
        >Statistics</a
      >
    </div>

    <div
      v-show="activeTab == 'load-files'"
      class="card w-full bg-base-200 shadow-xl rounded-t-none"
    >
      <load-files></load-files>
    </div>
    <div
      v-show="activeTab == 'statistics'"
      class="card w-full bg-base-200 shadow-xl rounded-t-none"
    >
      <statistics></statistics>
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
    <div class="flex flex-wrap gap-3 relative">
      <!-- eslint-disable-next-line vue/no-v-for-template-key -->
      <template v-for="file in filesStore.files" :key="file.identifier">
        <file-preview :file="file"></file-preview>
      </template>
    </div>
  </main>
</template>

<style scoped lang="scss">
</style>

