package highlighter.kotlinhighlighter

import KotlinLexer
import KotlinParser
import highlighter.Highlighter

class KotlinHighlighter : Highlighter(
    lexerOf = { KotlinLexer(it) },
    parserOf = { KotlinParser(it) },
    startRuleOf = { (it as KotlinParser).kotlinFile() },
    //
    lexicalHighlighter = KotlinLexicalHighlighter(),
    grammaticalHighlighter = KotlinGrammaticalHighlighter()
)
