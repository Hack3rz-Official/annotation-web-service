<script setup>
import FileDetailModalVue from "../components/FileDetailModal.vue";
import LoadFiles from "../components/LoadFiles.vue";
import FilePreview from "../components/FilePreview.vue"
import { useFilesStore } from "../stores/filesStore";
import { useLanguagesStore } from "../stores/languagesStore";

const filesStore = useFilesStore();
const languagesStore = useLanguagesStore();
</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <!-- FileDetailModal -->
    <file-detail-modal-vue></file-detail-modal-vue>

    <!-- LoadFiles -->
    <load-files></load-files>

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

