package resolver

import HTok
import LTok
import highlighter.Highlighter
import lexer.Lexer
import utils.toHighlightedHTML

abstract class Resolver (
    private val lexer: Lexer,
    private val highlighter: Highlighter
) {
    fun lex(src: String): Array<LTok>? =
        this.lexer.lex(src)

    fun highlight(src: String): Array<HTok>? =
        this.highlighter.highlight(src)

    fun debug(src: String): String? =
        this.highlighter.highlight(src)?.let { hToks ->
            toHighlightedHTML(hToks, src)
        }
}