<script setup>
import { ref, watch } from "vue";

import { useFilesStore } from "../stores/filesStore";
import { useLanguagesStore } from "../stores/languagesStore";
import { getBenchmarkFile } from "../composables/useFileFixtures";

const filesStore = useFilesStore();
const languagesStore = useLanguagesStore();

const sizes = ref(["small", "medium", "large"]);

function loadFile(language, size) {
  for (let i = 1; i <= 10; i++) {
    let file = getBenchmarkFile(language, size);
    filesStore.files.push(file);
  }
}
</script>

<template>
  <div class="card-body">
    <p>Add bundles of fixture files:</p>
    <div class="overflow-x-auto">
      <table class="table table-compact bg-transparent">
        <!-- head -->
        <thead>
          <tr>
            <th></th>
            <th>Small</th>
            <th>Medium</th>
            <th>Large</th>
          </tr>
        </thead>
        <tbody>
          <!-- row 1 -->
          <tr
            v-for="language of languagesStore.languages"
            :key="language.technical"
          >
            <th class="bg-transparent">{{ language.humanReadable }}</th>
            <td v-for="size of sizes" :key="size" class="bg-transparent">
              <button class="btn" @click="loadFile(language, size)">+10</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped lang="scss">
</style>
