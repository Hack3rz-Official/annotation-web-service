<script setup>
</script>

<template>
  <main class="container mx-auto px-3 gap-y-3">
    <!-- <h1 class="text-2xl py-4">Syntax Highlighting</h1> -->
    <p class="py-4">
      Highlight your Java, Python and Kotlin code with our Annotation Web
      Service. Highlight your Java, Python and Kotlin code with our Annotation
      Web Service. Highlight your Java, Python and Kotlin code with our
      Annotation Web Service.
    </p>
    <div class="flex flex-col gap-4 content-center w-full">
      <textarea
        id="code-input"
        name="code-input"
        rows="10"
        class="border-2 border-orange-400 p-2 w-full resize-none"
      >
public static void main(String[] args) {}
      </textarea>

      <div class="flex justify-center gap-2 w-min mx-auto">
        <select name="language-select" id="language-select">
          <option value="java">Java</option>
          <option value="python">Python</option>
          <option value="kotlin">Kotlin</option>
        </select>
        <p class="text-center w-min p-2 mx-auto border-2 border-orange-500">
          Translate
        </p>
      </div>

      <textarea
        id="code-output"
        name="code-output"
        rows="10"
        disabled
        class="border-2 border-orange-400 p-2 w-full resize-none"
      >
      </textarea>
    </div>
  </main>
</template>
