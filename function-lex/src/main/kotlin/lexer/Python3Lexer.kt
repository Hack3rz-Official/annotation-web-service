package lexer

import Python3Lexer

class Python3Lexer : Lexer(
    lexerOf = { Python3Lexer(it) }
)
