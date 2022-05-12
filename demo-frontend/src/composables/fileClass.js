import { axiosLimited, axiosDefault } from "./axios";
import { v4 as uuidv4 } from "uuid";
import { useSettingsStore } from "../stores/settingsStore";

// workaround to access pinia store outside component
let settingsStore = null
setTimeout(() => {
  settingsStore = useSettingsStore();
}, 1);
export default class File {
  static jsDelivrBaseUrl = "https://cdn.jsdelivr.net/gh/";

  constructor(githubUser, githubRepo, githubFile) {
    this.githubUser = githubUser;
    this.githubRepo = githubRepo;
    this.githubFile = githubFile;
    this.setLanguage(this.githubFile.split(".")[1]);
    this.identifier = this.computeIdentifier();
    this.uuid = uuidv4();
    this.rawCode = "";
    this.dirty = false;
    this.size = 0; // size of code in Bytes
    this.loc = 0; // lines of code
    this.highlightedCode = "";
    this.status = "empty"; // "empty", "raw", "loading", "highlighted"
    this.request = {
      startTimestamp: 0,
      endTimestamp: 0,
      duration: 0,
    };
  }

  setLanguage(language) {
    if (language == "py" || language == "python3" || language == "python") {
      this.languageShort = "py";
      this.languageLong = "python3";
    } else if (language == "java") {
      this.languageShort = "java";
      this.languageLong = "java";
    } else if (language == "kt" || language == "kotlin") {
      this.languageShort = "kt";
      this.languageLong = "kotlin";
    } else if (language == "go") {
      this.languageShort = "go";
      this.languageLong = "go";
    }
  }

  fetchRawCode() {
    // do not fetch again if already fetched
    if (this.rawCode != "") {
      return;
    }

    axiosDefault
      .get(`${File.jsDelivrBaseUrl}${this.identifier}`)
      .then((response) => {
        // console.log(response);
        this.rawCode = response.data;
        this.size = response.data.length;
        this.loc = this.computeLoc();
        this.status = "raw";
      })
      .catch((error) => {
        console.log(error);
        this.status = "empty";
      });
  }

  highlight() {
    //   console.log("requested highlighting for file", file);
    this.status = "loading";
    this.request.startTimestamp = Date.now();
    let data = {
      code: this.rawCode,
      language: this.languageLong,
    };
    let outputElem = null;
    if (!settingsStore.performanceMode) {
      outputElem = document.getElementById(this.uuid);
    }
    //   console.log(outputElem);

    axiosLimited
      .post(import.meta.env.VITE_HIGHLIGHT_URL, data)
      .then((response) => {
        if (!settingsStore.performanceMode) {
          let newElement = document
            .createRange()
            .createContextualFragment(response.data);
          outputElem.innerHTML = null;
          outputElem.appendChild(newElement);
        }
        //   console.log(newElement);
        //   console.log(outputElem);
        this.highlightedCode = response.data;
        this.status = "highlighted";
        this.dirty = false;
        this.request.endTimestamp = Date.now();
        this.request.duration = response.responseTime;
        console.log("actual response time: ", response.responseTime);
      })
      .catch((error) => {
        console.log(error);
        if (!settingsStore.performanceMode) {
          outputElem.innerHTML = "Error in Highlighting Service";
        }
        this.status = "failed";
        this.request.endTimestamp = Date.now();
        this.request.duration = response.responseTime;
        console.log("actual response time: ", response.responseTime);
      });
  }

  getFilenameShortened() {
    // very imperformant string manipulations, but it works
    let full = `${this.githubRepo}/${this.githubFile.split(".")[0]}`;
    let recBreaker = 0;
    while (full.length > 30 && recBreaker < 20) {
      let splitted = full.split("/");
      let repIndex = splitted.length - 2;

      splitted.splice(repIndex, 1);
      full = splitted.join("/");
      recBreaker += 1;
    }
    if (recBreaker == 1) {
      let splitted = full.split("/");
      splitted.splice(splitted.length - 1, 0, "..");
      full = splitted.join("/");
    } else if (recBreaker > 1) {
      let splitted = full.split("/");
      splitted.splice(splitted.length - 1, 0, "...");
      full = splitted.join("/");
    }
    return full;
  }

  computeIdentifier() {
    return `${this.githubUser}/${this.githubRepo}/${this.githubFile}`;
  }

  getSizeFormatted() {
    return `${Math.round((this.size / 1000) * 10) / 10} kB`;
  }

  computeLoc() {
    return this.rawCode.split("\n").length;
  }
}
