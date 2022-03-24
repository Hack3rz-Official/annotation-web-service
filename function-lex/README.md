# Lex Function

## Prerequisites
1. Install Java Developer Kit (Version 8)
2. Install Azure CLI
3. Install Azure Functions Core Tools (version 2.6.666 or above)
4. Install Gradle (version 6.8 and above)



------

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
