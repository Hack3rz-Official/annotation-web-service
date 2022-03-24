package highlighter.javahighlighter

import highlighter.Highlighter
import Java8Lexer
import Java8Parser

class JavaHighlighter: Highlighter(
    lexerOf = { Java8Lexer(it) },
    parserOf = { Java8Parser(it) },
    startRuleOf = { (it as Java8Parser).compilationUnit() },
    //
    lexicalHighlighter = JavaLexicalHighlighter(),
    grammaticalHighlighter = JavaGrammaticalHighlighter()
)
