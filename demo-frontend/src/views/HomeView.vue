<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const inputCode = ref("public static void main(String[] args) {}");
const languageOptions = ref(["java", "python3", "kotlin"]);
const selectedLanguage = ref("java");

function highlight() {
  let data = {
    code: inputCode.value,
    language: selectedLanguage.value,
  };
  let outputElem = document.getElementById("code-output");
  outputElem.innerHTML = null;
  axios
    .post("http://localhost:3000/highlight", data)
    .then((response) => {
      let newElement = document
        .createRange()
        .createContextualFragment(response.data);
      outputElem.appendChild(newElement);
    })
    .catch((error) => {
      console.log(error);
      outputElem.innerHTML = 'Error in Highlighting Service'
    });
}

function loadRandomCode() {
  let randomCode = getRandomCode();
  inputCode.value = randomCode;
  highlight();
}

function getRandomCode() {
  if (selectedLanguage.value == "java") {
    return `import java.util.Scanner;

public class HelloWorld {

    public static void main(String[] args) {

        Scanner reader = new Scanner(System.in);
        System.out.print("Enter a number: ");

        // nextInt() reads the next integer from the keyboard
        int number = reader.nextInt();

        System.out.println("You entered: " + number);
    }
}`;
  } else if (selectedLanguage.value == "python3") {
    return `# This program adds two numbers

num1 = 1.5
num2 = 6.3

# Add two numbers
sum = num1 + num2

# Display the sum
print('The sum of {0} and {1} is {2}'.format(num1, num2, sum))`;
  } else if (selectedLanguage.value == "kotlin") {
    return `fun main() {
    val name = "stranger"        // Declare your first variable
    println("Hi, $name!")        // ...and use it!
    print("Current count:")
    for (i in 0..10) {           // Loop over a range from 0 to 10
        print(" $i")
    }
}`;
  }
}

onMounted(() => {
  loadRandomCode();
});
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

    <div class="w-full flex flex-wrap justify-start gap-4 mb-4">
      <label for="language-select">Language:</label>
      <select
        name="language-select"
        id="language-select"
        v-model="selectedLanguage"
      >
        <option
          v-for="language in languageOptions"
          :key="language"
          :value="language"
        >
          {{ language }}
        </option>
      </select>
      <div class="border-2 p-2 cursor-pointer" @click="loadRandomCode">
        Load random code snippet
      </div>
    </div>

    <div class="flex flex-col gap-4 content-center w-full lg:flex-row">
      <textarea
        id="code-input"
        name="code-input"
        rows="10"
        class="border-2 border-orange-400 p-2 w-full resize-none"
        v-model="inputCode"
      ></textarea>

      <div class="flex justify-center gap-2 w-min mx-auto lg:flex-col">
        <p
          class="
            text-center
            w-min
            p-2
            mx-auto
            border-2 border-orange-500
            cursor-pointer
          "
          @click="highlight"
        >
          Highlight
        </p>
      </div>

      <div
        id="code-output"
        name="code-output"
        class="border-2 border-orange-400 p-2 w-full"
      ></div>
    </div>
  </main>
</template>
