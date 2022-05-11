<script setup>
import { ref, watch } from "vue";
import { useFilesStore } from "../stores/filesStore";
import { useLanguagesStore } from "../stores/languagesStore";

const filesStore = useFilesStore();
const languagesStore = useLanguagesStore();
const editMode = ref(true);
const selectedLanguage = ref(null);

filesStore.$subscribe((mutation, state) => {
  // prevent updates when file is being edited
  if (filesStore.activeFile && filesStore.activeFile.dirty) {
    return
  }

  // make sure edit mode is on when file is not highlighted yet
  if (!filesStore.activeFile || filesStore.activeFile.status != "highlighted") {
    editMode.value = true;
  } else {
    editMode.value = false;
    // if the modal gets opened in highlighted state, we need to manually trigger the element
    setTimeout(() => {
      updateHighlightedCodeDisplay();
    }, 20);
  }
  if (filesStore.activeFile) {
    // match language selection with current file
    selectedLanguage.value = filesStore.activeFile.languageLong;
  }
});

watch(selectedLanguage, (newSelectedLanguage, oldSelectedLanguage) => {
  filesStore.activeFile.setLanguage(newSelectedLanguage);
});

function setFileDirty() {
  filesStore.activeFile.dirty = true;
}

function toggleEditModeOn() {
  editMode.value = true;
}

function toggleEditModeOff() {
  editMode.value = false;
  updateHighlightedCodeDisplay();
}

function updateHighlightedCodeDisplay() {
  let outputElem = document.getElementById("active-file-highlighted");
  let newElement = document
    .createRange()
    .createContextualFragment(filesStore.activeFile.highlightedCode);
  outputElem.innerHTML = null;
  outputElem.appendChild(newElement);
}
</script>

<template>
  <div
    class="modal h-11/12"
    :class="{ 'modal-open': filesStore.activeFile }"
    @click="filesStore.setActiveFile(null)"
    v-if="filesStore.activeFile"
  >
    <div
      class="modal-box relative h-full w-11/12 max-w-7xl"
      @click.stop="() => {}"
    >
      <div class="flex flex-row-reverse gap-4 w-full h-full">
        <!-- sidebar -->
        <div class="w-48 flex flex-col gap-4 justify-between">
          <div class="flex flex-col gap-4">
            <!-- editMode toggle -->
            <div class="form-control">
              <div class="input-group">
                <button
                  class="btn btn- w-1/2"
                  :class="{ 'btn-outline': !editMode }"
                  @click="toggleEditModeOn"
                >
                  Edit
                </button>
                <button
                  class="btn btn- w-1/2"
                  :class="{ 'btn-outline': editMode }"
                  @click="toggleEditModeOff"
                >
                  Preview
                </button>
              </div>
            </div>

            <button
              class="btn btn-primary w-full"
              @click="filesStore.activeFile.highlight()"
            >
              Save & Highlight
            </button>

            <select
              class="select select-primary w-full max-w-xs"
              v-model="selectedLanguage"
            >
              <!-- <option disabled selected>Select language</option> -->
              <option
                v-for="language in languagesStore.languagesExtendedWithGo"
                :key="language"
                :value="language.technical"
              >
                {{ language.humanReadable }}
              </option>    
            </select>
          </div>

          <button class="btn w-full" @click="filesStore.setActiveFile(null)">
            Close
          </button>
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
              v-model="filesStore.activeFile.rawCode"
              @keypress="setFileDirty()"
            ></textarea>
          </div>

          <div
            class="card-body mt-3 h-full"
            v-show="!editMode && filesStore.activeFile.status == 'highlighted'"
          >
            <div
              id="active-file-highlighted"
              wrap="off"
              class="resize-none font-mono text-sm bg-transparent overflow-auto"
              disabled
            ></div>
          </div>

          <div
            class="card-body mt-3 h-full flex flex-col justify-center items-center"
            v-show="!editMode && filesStore.activeFile.status != 'highlighted'"
          >
            <p class="grow-0 font-semibold">This File has not been highlighted yet.</p>
            <button
              class="btn btn-primary m-4 px-6"
              @click="filesStore.activeFile.highlight()"
            >
              Highlight
            </button>
          </div>

          <!-- file name badge -->
          <div
            class="badge w-full h-6 absolute rounded-none"
            :class="{
              'badge-success': filesStore.activeFile.status == 'highlighted',
              'badge-warning': filesStore.activeFile.status == 'loading',
              'badge-error': filesStore.activeFile.status == 'failed',
            }"
          >
            {{ filesStore.activeFile.getFilenameShortened() }}.<span
              class="font-bold"
              >{{ filesStore.activeFile.languageShort }}</span
            >
          </div>
        </div>
      </div>

      <!-- modal content end -->
    </div>
  </div>
</template>

<style scoped lang="scss">
.text-tiny {
  font-size: 6px;
  line-height: 6px;
}
</style>
