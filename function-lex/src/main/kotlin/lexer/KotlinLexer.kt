package lexer

import KotlinLexer

class KotlinLexer : Lexer(
    lexerOf = { KotlinLexer(it) }
)
