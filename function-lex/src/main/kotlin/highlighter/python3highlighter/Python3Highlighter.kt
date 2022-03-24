package highlighter.python3highlighter

import Python3Lexer
import Python3Parser
import highlighter.Highlighter

class Python3Highlighter : Highlighter(
    lexerOf = { Python3Lexer(it) },
    parserOf = { Python3Parser(it) },
    startRuleOf = { (it as Python3Parser).file_input() },
    //
    lexicalHighlighter = Python3LexicalHighlighter(),
    grammaticalHighlighter = Python3GrammaticalHighlighter()
)
