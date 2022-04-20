<script setup>
import { ref } from "vue";

const props = defineProps({
  activeFile: {
    type: Object,
    required: true,
  },
});

const editMode = ref(true);

function toggleEditMode() {
  editMode.value = !editMode.value;

  if (!editMode.value) {
    let outputElem = document.getElementById("active-file-highlighted");
    let newElement = document
      .createRange()
      .createContextualFragment(props.activeFile.highlightedCode);
    outputElem.innerHTML = null;
    outputElem.appendChild(newElement);
  }
}
</script>

<template>
  <div
    class="modal h-11/12"
    :class="{ 'modal-open': activeFile }"
    @click="$emit('closeFileModal')"
    v-if="activeFile"
  >
    <div
      class="modal-box relative h-full w-11/12 max-w-7xl"
      @click.stop="() => {}"
    >
      <label
        class="btn btn-sm btn-circle absolute right-2 top-2"
        @click="$emit('closeFileModal')"
        >✕</label
      >
      <!-- modal content start -->

      <div class="flex flex-row-reverse gap-4 w-full h-full">
        <!-- sidebar -->
        <div class="w-48 flex flex-col gap-4 justify-between">
          <div class="flex flex-col gap-4">
            <!-- editMode toggle -->
            <button class="btn btn-primary w-full" :class="{ 'btn-outline': !editMode }" @click="toggleEditMode()" :disabled="activeFile.status != 'highlighted'">
              Toggle Edit Mode
            </button>
            <button class="btn btn-primary w-full" @click="$emit('highlightFile')">
              Highlight
            </button>

            <select class="select select-info w-full max-w-xs">
              <option disabled selected>Select language</option>
              <option>English</option>
              <option>Japanese</option>
              <option>Italian</option>
            </select>
          </div>

          <button class="btn w-full" @click="() => {}">Close</button>
        </div>
        <!-- code area -->
        <div
          class="
            card card-compact
            w-10/12 w-max-md
            h-full
            bg-base-200
            shadow-md
            border-2
          "
        >
          <div class="card-body mt-3 h-full" v-show="editMode">
            <textarea
              id="raw-code"
              wrap="off"
              class="
                resize-none
                font-mono
                text-sm
                bg-transparent
                overflow-auto
                h-full
              "
              v-model="activeFile.rawCode"
            ></textarea>
          </div>

          <div class="card-body mt-3 h-full" v-show="!editMode">
            <div
              id="active-file-highlighted"
              wrap="off"
              class="resize-none font-mono text-sm bg-transparent overflow-auto"
              disabled
            ></div>
          </div>
          <!-- file name badge -->
          <div
            class="badge w-full h-6 absolute rounded-none"
            :class="{
              'badge-success': activeFile.status == 'highlighted',
              'badge-warning': activeFile.status == 'loading',
              'badge-error': activeFile.status == 'failed',
            }"
          >
            {{ activeFile.getFilenameShortened() }}.<span class="font-bold">{{
              activeFile.languageShort
            }}</span>
          </div>
        </div>
      </div>

      <!-- modal content end -->
    </div>
  </div>
</template>

<style scoped lang="scss">
// .file-wrapper {
//   height: 400px;
//   width: 290px;
//   .card-body {
//     height: calc(100% - 50px);
//     div,
//     textarea {
//       height: 100%;
//     }
//   }
// }

.text-tiny {
  font-size: 6px;
  line-height: 6px;
}
</style>
