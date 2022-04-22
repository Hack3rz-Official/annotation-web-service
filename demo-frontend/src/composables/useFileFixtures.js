import File from "./fileClass";


export function useFileFixtures() {
  let java1 = new File("elastic", "elasticsearch", "server/src/main/java/org/elasticsearch/action/index/IndexAction.java");
  let java2 = new File("elastic", "elasticsearch", "server/src/main/java/org/elasticsearch/action/index/IndexRequest.java");
  let java3 = new File("elastic", "elasticsearch", "server/src/main/java/org/elasticsearch/action/index/IndexResponse.java");

  let python1 = new File("pallets", "flask", "src/flask/views.py");
  let python2 = new File("pallets", "flask", "src/flask/typing.py");
  let python3 = new File("pallets", "flask", "src/flask/sessions.py");

  let kotlin1 = new File("JetBrains", "kotless", "model/src/main/kotlin/io/kotless/HTTP.kt")
  let kotlin2 = new File("JetBrains", "kotless", "model/src/main/kotlin/io/kotless/Event.kt")
  let kotlin3 = new File("JetBrains", "kotless", "model/src/main/kotlin/io/kotless/Permission.kt")

  return [java1, java2, java3, python1, python2, python3, kotlin1, kotlin2, kotlin3]
}
