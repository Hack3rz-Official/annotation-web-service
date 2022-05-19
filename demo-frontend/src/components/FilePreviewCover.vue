<script setup>
import { useFilesStore } from "../stores/filesStore";
import { useLanguagesStore } from "../stores/languagesStore";
import { useSettingsStore } from "../stores/settingsStore";
import { ref, computed } from "vue";
import { computePercentage } from "../composables/mathHelpers";

const filesStore = useFilesStore();
const languagesStore = useLanguagesStore();
const settingsStore = useSettingsStore();

const props = defineProps({
  language: {
    type: Object,
    required: true,
  },
  files: {
    type: Array,
    requred: true,
  },
});

const filesTotal = computed(() => {
  return props.files.length;
});

const filesHighlighted = computed(() => {
  return props.files.filter((file) => {
    return file.status == "highlighted";
  }).length;
});
</script>

<template>
  <div class="file-wrapper card card-compact bg-base-200 border-primary shadow-xl border-2 absolute left-0 z-10">
    <!-- this card-body is shown when there is only raw code -->
    <div class="card-body mt-3 flex flex-column justify-between items-center">
      <h2 class="card-title">{{ language.humanReadable }}</h2>

      <div
        class="radial-progress text-primary font-bold text-lg"
        :style="{ '--value': computePercentage(filesTotal, filesHighlighted) }"
        style="--size:8rem; --thickness: 14px;"
      >
        {{ filesHighlighted }} / {{ filesTotal }}
      </div>

      <button
        class="btn btn-primary btn-primary my-2 w-full"
        @click="filesStore.highlightSelectedFiles(files)"
      >
        highlight all
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.file-wrapper {
  height: 400px;
  width: 200px;
  min-width: 200px;
  .card-body {
    height: calc(100% - 50px);
  }
}

.text-tiny {
  font-size: 6px;
  line-height: 6px;
}

.card {
  //   transform: translate(100px);
  transition: 0.2s;
}

.card:hover {
  // transform: translateY(-0.5rem);
}

.card:focus-within ~ .card,
.card:hover ~ .card {
  transform: translateX(-0px);
}

.card:not(:first-child) {
  margin-right: -100px;
}
</style>
