package lexer

import LTok
import org.antlr.v4.runtime.*
import org.antlr.v4.runtime.Lexer

abstract class Lexer(
    private val lexerOf: (CharStream) -> Lexer,
) {
    fun lex(src: String): Array<LTok>? =
        try {
            val lexer = lexerOf(CharStreams.fromString(src))
            lexer.removeErrorListeners()
            lexer.allTokens
                .map { LTok(it.startIndex, it.stopIndex, it.type) }
                .sortedBy { it.startIndex }
                .toTypedArray()
        } catch (e: Exception) {
            null
        }
}