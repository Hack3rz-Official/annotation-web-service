<script setup>
import { useFilesStore } from "../stores/filesStore";
import { useLanguagesStore } from "../stores/languagesStore";
import { useSettingsStore } from "../stores/settingsStore";

const filesStore = useFilesStore();
const languagesStore = useLanguagesStore();
const settingsStore = useSettingsStore();

defineProps({
  file: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <div
    class="
      file-wrapper
      card card-compact
      w-full
      bg-base-200
      shadow-xl
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
    <div
      class="card-body mt-3"
      v-show="
        !file.highlightedCode ||
        (file.highlightedCode && settingsStore.performanceMode)
      "
    >
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
    <div
      class="card-body mt-3"
      v-show="!settingsStore.performanceMode && file.highlightedCode"
    >
      <div
        :id="file.uuid"
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
    <div class="absolute w-full h-8 rounded rounded-t-none border-0 bottom-0">
      <div v-if="file.request.duration > 0" class="badge absolute m-2 right-0">
        {{ file.request.duration }} ms
      </div>
      <div class="badge absolute m-2 left-0">{{ file.loc }} lines</div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.file-wrapper {
  height: 400px;
  width: 290px;
  min-width: 200px;
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

.card {
  transform: translate(100px);
  transition: 0.2s
}

.card:hover {
    // transform: translateY(-0.5rem);
}

.card:focus-within~.card, .card:hover~.card {
    transform: translateX(-0px);
}

.card:not(:first-child) {
    margin-right: -100px;
}
</style>
