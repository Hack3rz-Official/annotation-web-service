package resolver

import highlighter.javahighlighter.JavaHighlighter
import lexer.JavaLexer

class JavaResolver : Resolver(
    lexer = JavaLexer(),
    highlighter = JavaHighlighter()
)
