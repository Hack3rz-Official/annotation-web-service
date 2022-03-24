package resolver

import highlighter.kotlinhighlighter.KotlinHighlighter
import lexer.KotlinLexer

class KotlinResolver : Resolver(
    lexer = KotlinLexer(),
    highlighter = KotlinHighlighter()
)
