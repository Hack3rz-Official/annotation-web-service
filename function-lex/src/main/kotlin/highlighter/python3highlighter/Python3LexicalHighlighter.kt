package highlighter.python3highlighter

import HTok
import LTok
import highlighter.LexicalHighlighter
import Python3Lexer
import HCode

class Python3LexicalHighlighter: LexicalHighlighter(lexer.Python3Lexer()) {

    private val keywords =
        hashSetOf(
            Python3Lexer.DEF, Python3Lexer.RETURN, Python3Lexer.RAISE, Python3Lexer.FROM,
            Python3Lexer.IMPORT, Python3Lexer.AS, Python3Lexer.GLOBAL, Python3Lexer.NONLOCAL,
            Python3Lexer.ASSERT, Python3Lexer.IF, Python3Lexer.ELIF, Python3Lexer.ELSE,
            Python3Lexer.WHILE, Python3Lexer.FOR, Python3Lexer.IN, Python3Lexer.TRY,
            Python3Lexer.FINALLY, Python3Lexer.WITH, Python3Lexer.EXCEPT, Python3Lexer.LAMBDA,
            Python3Lexer.OR, Python3Lexer.AND, Python3Lexer.NOT, Python3Lexer.IS, Python3Lexer.NONE,
            Python3Lexer.CLASS, Python3Lexer.YIELD, Python3Lexer.DEL, Python3Lexer.PASS,
            Python3Lexer.CONTINUE, Python3Lexer.BREAK, Python3Lexer.ASYNC, Python3Lexer.AWAIT
        )

    private val literals =
        hashSetOf(
            Python3Lexer.TRUE, Python3Lexer.FALSE, Python3Lexer.NUMBER
        )

    private val stringLiterals =
        hashSetOf(
            Python3Lexer.STRING
        )

    private val comments =
        hashSetOf(
            Python3Lexer.HIDDEN_COMMENT
        )

    override fun hCodeOf(lTok: LTok): HTok =
        when (lTok.tokenId) {
            in keywords -> HTok(lTok, HCode.KEYWORD)
            in literals -> HTok(lTok, HCode.LITERAL)
            in stringLiterals -> HTok(lTok, HCode.CHAR_STRING_LITERAL)
            in comments -> HTok(lTok, HCode.COMMENT)
            else -> HTok(lTok, HCode.ANY)
        }
}
