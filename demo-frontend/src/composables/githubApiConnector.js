import { axiosDefault } from "./axios";

const GITHUB_API_URL = "https://api.github.com";

export async function getCommitsFromRepo(owner, repo) {
  try {
    const response = await axiosDefault.get(
      `${GITHUB_API_URL}/repos/${owner}/${repo}/commits`
    );
    return response.data[0].sha;
  } catch (err) {
    console.error(err);
  }
}

export async function getFilesFromTree(owner, repo, tree_sha) {
  try {
    const response = await axiosDefault.get(
      `${GITHUB_API_URL}/repos/${owner}/${repo}/git/trees/${tree_sha}?recursive=true`
    );
    return response.data.tree;
  } catch (err) {
    console.error(err);
  }
}

export function sortTreeByLanguages(tree) {
const dict = {}
  for (let node of tree) {
    if (node.type == "tree") {
      continue;
    }
    let extension = node.path.split(".").at(-1);
    if (extension in dict) {
        dict[extension].push(node.path)
    } else {
        dict[extension] = [node.path]
    }
  }
  return dict
}
