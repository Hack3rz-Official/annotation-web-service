package highlighter

import lexer.Lexer
import HTok
import LTok

abstract class LexicalHighlighter(
    private val lexer: Lexer
) {
    abstract fun hCodeOf(lTok: LTok) : HTok

    fun highlight(src: String): Collection<HTok>? =
        lexer.lex(src)?.map { hCodeOf(it) }
}
