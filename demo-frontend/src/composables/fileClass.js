export default class File {
  static jsDelivrBaseUrl = "https://cdn.jsdelivr.net/gh/";

  constructor(githubUser, githubRepo, githubFile) {
    this.githubUser = githubUser;
    this.githubRepo = githubRepo;
    this.githubFile = githubFile;
    this.language = this.getLanguageFromFilename();
    this.identifier = this.computeIdentifier();
    this.rawCode = "";
    this.highlightedCode = "";
    this.status = "empty" // "empty", "raw", "loading", "highlighted"
    this.request = {
        startTimestamp: 0,
        endTimestamp: 0,
        duration: 0,
    }
  }

  getLanguageFromFilename() {
    const fileType = this.githubFile.split(".")[1]
    if (fileType == 'java') { return 'java' }
    else if (fileType == 'py') { return 'python3' }
    else if (fileType == 'kt') { return 'kotlin' }
  }

  computeIdentifier() {
    return `${this.githubUser}/${this.githubRepo}/${this.githubFile}`;
  }
}
