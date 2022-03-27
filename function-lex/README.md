# Lex Function

## Prerequisites

#### 1. Install Java Developer Kit (Version 8)

#### 2. Install [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/)

For macOS: `brew update && brew install azure-cli` (make sure you have [Homebrew](https://brew.sh/) installed)

#### 3. Install [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cmacos%2Ccsharp%2Cportal%2Cbash#v2) (version 2.6.666 or above)
```bash
brew tap azure/functions
brew install azure-functions-core-tools@4
# if upgrading on a machine that has 2.x or 3.x installed:
brew link --overwrite azure-functions-core-tools@4
```

#### 4. Install [Gradle](https://gradle.org/install/) (version 6.8 and above)
For macOs: `brew install gradle`

## Run the Function Locally
Run the following command to build then run the function project (make sure you're in the folder of the cloud function and not in the repo's root):
```bash
gradle jar --info
gradle azureFunctionsRun
```
Trigger the function from the command line using the following cURL command in a new terminal window:

```bash
curl -w "\n" http://localhost:7071/api/lex --data 'public static void main(String args[]){}'
```


## Deployment
Make sure that Azure CLI is installed and that you're authenticated (use `az login`)

Package the function using:
```bash
gradle azureFunctionsPackageZip
```
Then deploy it using:
```bash
gradle azureFunctionsDeploy
```
This will use the app settings described in the `build.gradle` file.

----
Readme.md of Original Java Cloud Function Example of Azure
----

---
page_type: sample
languages:
- java
  products:
- azure-functions
- azure
  description: "This repository contains sample for Azure Functions in Java"
  urlFragment: "azure-functions-java"
---

# Azure Functions samples in Java

This repository contains samples which show the basis usage of [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/) in Java.

## Contents

Outline the file contents of the repository. It helps users navigate the codebase, build configuration and any related assets.

| File/folder    | Description                                      |
|----------------|--------------------------------------------------|
| `src`          | Sample source code.                              |
| `.gitignore`   | Define what to ignore at commit time.            |
| `build.gradle` | The gradle configuration to this sample.         |
| `host.json`    | The host.json metadata file contains configuration options that affect all functions in a function app instance.  [Docs](https://github.com/Azure/azure-functions-host/wiki/host.json-(v2)) |
| `README.md`    | This README file.                                |

## Prerequisites

- Gradle 4.10+
- Latest [Function Core Tools](https://aka.ms/azfunc-install)
- Azure CLI. This plugin use Azure CLI for authentication, please make sure you have Azure CLI installed and logged in.

## Setup

- ```cmd
    az login
    az account set -s <your subscription id>
    ```
- Update the Application settings in Azure portal with the required parameters as below
    - AzureWebJobsStorage: Connection string to your storage account
    - CosmosDBDatabaseName: Cosmos database name. Example: ItemCollectionIn
    - CosmosDBCollectionName:Cosmos database collection name. Example: ItemDb
    - AzureWebJobsCosmosDBConnectionString: Connection string to your Cosmos database
    - AzureWebJobsEventGridOutputBindingTopicUriString: Event Grid URI
    - AzureWebJobsEventGridOutputBindingTopicKeyString: Event Grid string
    - AzureWebJobsEventHubSender, AzureWebJobsEventHubSender_2 : Event hub connection string
    - AzureWebJobsServiceBus: Service bus connection string
    - SBQueueName: Service bus queue name. Example: test-input-java
    - SBTopicName: Service bus topic name. Example: javaworkercitopic2
    - SBTopicSubName: Service bus topic name. Example: javaworkercisub
- Update `host.json` with the right extension bundle version. `V3 - [1.*, 2.0.0) and V4 - [2.*, 3.0.0)`

## Running the sample

```cmd
./mvnw clean package azure-functions:run
```

```cmd
./gradlew clean azureFunctionsRun
```

## Deploy the sample on Azure


```cmd
./mvnw clean package azure-functions:deploy
```

```cmd
./gradlew clean azureFunctionsDeploy
```

> NOTE: please replace '/' with '\\' when you are running on windows.

------
Readme.md of original Java Library
-----

# ASE: Annotation Formal Model

This Java library allows for the formal computation of syntax highlighting patterns of input programs.
Hence, syntax highlighting is computed by analysing the Abstract Syntax Tree (AST) corresponding to the input provided.
Although for the derivation of the AST some minor imprecision are allowed, a high level of grammatical errors in the language derivation provided will lead this process to fail gracefully.
The library supports Java (1.8 or later), Python (3.x or later) and Kotlin (1.x or later).

Note:  consider importing it as a library in your implementation, this is available as a `.jar` file in `Library/SHOracle.jar`.


## Lexing
Lexing is the process of deriving the annotated token sequence of an input file.
This functionality is made available in the `Resolve` objects in the `resolver` package.
For example:
```java
import resolver.Python3Resolver;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        Python3Resolver resolver = new Python3Resolver();
        LTok[] lToks = resolver.lex("public class Test {}");
        System.out.println(Arrays.toString(lToks));
    }
}
```
is the implementation for obtaining the sequence of `LTok` objects of the input code `public class Test {}`.
`LTok` objects carry information about a token's location and id (ie. type according to the language's grammar, useful to the Deep Learning modules for both learning and prediction).
Hence, the above code outputs the following:
```txt
[LTok{startIndex=0, endIndex=5, tokenId=42}, LTok{startIndex=7, endIndex=11, tokenId=33}, LTok{startIndex=13, endIndex=16, tokenId=42}, LTok{startIndex=18, endIndex=18, tokenId=74}, LTok{startIndex=19, endIndex=19, tokenId=75}]
```

## Highlighting
Highlighting is the process of binding to each token of an input sequence a grammatical highlighting code (or type).
This functionality is exposed by the `Resolve` objects of each language. For example:
```java
import resolver.Python3Resolver;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        Python3Resolver resolver = new Python3Resolver();
        HTok[] hToks = resolver.highlight("public class Test {}");
        System.out.println(Arrays.toString(hToks));
    }
}
```
is the implementation for obtaining the sequence of `HTok` of the input code `public class Test {}`.
`HTok` extends a `LTok` object to include the highlighting value of a particular token.
This property is referred to as the `hCodeValue` value of a token.
The above code outputs the following:
```txt
[HTok{hCodeValue=0, startIndex=0, endIndex=5, tokenId=42}, HTok{hCodeValue=1, startIndex=7, endIndex=11, tokenId=33}, HTok{hCodeValue=5, startIndex=13, endIndex=16, tokenId=42}, HTok{hCodeValue=0, startIndex=18, endIndex=18, tokenId=74}, HTok{hCodeValue=0, startIndex=19, endIndex=19, tokenId=75}, HTok{hCodeValue=0, startIndex=20, endIndex=19, tokenId=-1}]
```
`hCodeValue` values are instances of the enum class `HCode`; executing the following code:

```java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        System.out.println(Arrays.toString(HCode.values()));
    }
}
```

yields the bindings for all highlighting code values:
```txt
[HCode{name=ANY, hCodeValue=0}, HCode{name=KEYWORD, hCodeValue=1}, HCode{name=LITERAL, hCodeValue=2}, HCode{name=CHAR_STRING_LITERAL, hCodeValue=3}, HCode{name=COMMENT, hCodeValue=4}, HCode{name=CLASS_DECLARATOR, hCodeValue=5}, HCode{name=FUNCTION_DECLARATOR, hCodeValue=6}, HCode{name=VARIABLE_DECLARATOR, hCodeValue=7}, HCode{name=TYPE_IDENTIFIER, hCodeValue=8}, HCode{name=FUNCTION_IDENTIFIER, hCodeValue=9}, HCode{name=FIELD_IDENTIFIER, hCodeValue=10}, HCode{name=ANNOTATION_DECLARATOR, hCodeValue=11}]
```

## Debugging
`Resolver` objects expose some base functionality to visually debug the highlighting output (ie. `HTok` sequences) of each highlighter.
You should find the following implementation to output the HTML rendering of the passed in Python code.
```java
import resolver.Python3Resolver;

public class Main {
    public static void main(String[] args) {
        Python3Resolver python3Resolver = new Python3Resolver();
        String htmlOutput = python3Resolver.debug("def func(txt: str) -> str:\n\treturn str * 2\n");
        System.out.println(htmlOutput);
    }
}
```
