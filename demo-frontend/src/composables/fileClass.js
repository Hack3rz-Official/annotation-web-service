export default class File {
  static jsDelivrBaseUrl = "https://cdn.jsdelivr.net/gh/";

  constructor(githubUser, githubRepo, githubFile) {
    this.githubUser = githubUser;
    this.githubRepo = githubRepo;
    this.githubFile = githubFile;
    this.languageShort = this.githubFile.split(".")[1]
    this.languageLong = this.getLanguageLongFromFilename();
    this.identifier = this.computeIdentifier();
    this.rawCode = "";
    this.size = 0; // size of code in Bytes
    this.highlightedCode = "";
    this.status = "empty" // "empty", "raw", "loading", "highlighted"
    this.request = {
        startTimestamp: 0,
        endTimestamp: 0,
        duration: 0,
    }
  }

  getLanguageLongFromFilename() {
    const fileType = this.githubFile.split(".")[1]
    if (fileType == 'java') { return 'java' }
    else if (fileType == 'py') { return 'python3' }
    else if (fileType == 'kt') { return 'kotlin' }
  }

  getFilenameShortened() {
    // very imperformant string manipulations, but it works
    let full = `${this.githubRepo}/${this.githubFile.split(".")[0]}`
    let recBreaker = 0
    while (full.length > 30 && recBreaker < 10) {
      let splitted = full.split("/")
      let repIndex = splitted.length - 2
      
      splitted.splice(repIndex, 1)
      full = splitted.join('/')
      recBreaker += 1
    }
    if (recBreaker == 1) {
      let splitted = full.split("/")
      splitted.splice(splitted.length-1, 0, '..')
      full = splitted.join('/')
    } else if (recBreaker > 1) {
      let splitted = full.split("/")
      splitted.splice(splitted.length-1, 0, '...')
      full = splitted.join('/')
    }
    return full
  }

  computeIdentifier() {
    return `${this.githubUser}/${this.githubRepo}/${this.githubFile}`;
  }

  getSizeFormatted() {
    return `${Math.round(this.size / 1000 * 10) / 10} kB`
  }
}
