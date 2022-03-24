package resolver

import highlighter.python3highlighter.Python3Highlighter
import lexer.Python3Lexer

class Python3Resolver : Resolver(
    lexer = Python3Lexer(),
    highlighter = Python3Highlighter()
)
