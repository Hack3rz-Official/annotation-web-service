package lexer

import Java8Lexer
import Java8Parser

class JavaLexer : Lexer(
    lexerOf = { Java8Lexer(it) }
)