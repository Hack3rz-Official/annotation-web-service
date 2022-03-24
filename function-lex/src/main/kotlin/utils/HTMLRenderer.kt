package utils

import HCode
import HTok

fun String.inHTMLFile(): String =
    """
<!DOCTYPE html>
<html>
<style>
.ANY {
    color: black;
    font-weight: normal;
    font-style: normal;
}
.KEYWORD {
    color: blue;
    font-weight: bold;
    font-style: normal;
}
.LITERAL {
    color: lightskyblue;
    font-weight: bold;
    font-style: normal;
}
.CHAR_STRING_LITERAL {
    color: darkgoldenrod;
    font-weight: normal;
    font-style: normal;
}
.COMMENT {
    color: grey;
    font-weight: normal;
    font-style: italic;
}
.CLASS_DECLARATOR {
    color: crimson;
    font-weight: bold;
    font-style: normal;
}
.FUNCTION_DECLARATOR {
    color: fuchsia;
    font-weight: bold;
    font-style: normal;
}
.VARIABLE_DECLARATOR {
    color: purple;
    font-weight: bold;
    font-style: normal;
}
.TYPE_IDENTIFIER {
    color: darkgreen;
    font-weight: bold;
    font-style: normal;
}
.FUNCTION_IDENTIFIER {
    color: dodgerblue;
    font-weight: normal;
    font-style: normal;
}
.FIELD_IDENTIFIER {
    color: coral;
    font-weight: normal;
    font-style: normal;
}
.ANNOTATION_DECLARATOR {
    color: lightslategray;
    font-weight: lighter;
    font-style: italic;
}
</style>
<pre>
$this
</pre>
</html>
""".trimIndent()

fun String.inHTML(hcode: HCode): String =
    hcode.name.let { tag -> "<code class=\"$tag\">$this</code>"}

fun toHighlightedHTML(hetas: Array<HTok>, text: String): String =
    StringBuilder(text.length + (hetas.size * 14)).let { stringBuilder ->
        var currTokenIndex = 0
        var currCharIndex = 0
        while (currCharIndex < text.length) {
            while (currTokenIndex < hetas.size - 1 && hetas[currTokenIndex].startIndex < currCharIndex)
                currTokenIndex += 1
            if (currTokenIndex > hetas.lastIndex) {
                stringBuilder.append(text[currCharIndex])
                ++currCharIndex
            }
            else
                when (currCharIndex) {
                    hetas[currTokenIndex].startIndex -> {
                        val t = hetas[currTokenIndex]
                        val ttxt = text.subSequence(t.startIndex, t.endIndex + 1).toString()
                        stringBuilder.append(ttxt.inHTML(HCode.values()[t.hCodeValue]))
                        currCharIndex += ttxt.length
                        ++currTokenIndex
                    }
                    else -> {
                        stringBuilder.append(text[currCharIndex])
                        ++currCharIndex
                    }
                }
        }
        stringBuilder.toString().inHTMLFile()
    }
