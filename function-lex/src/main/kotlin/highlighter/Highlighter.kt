package highlighter

import HTok
import LTok
import org.antlr.v4.runtime.*
import org.antlr.v4.runtime.tree.ParseTreeWalker
import java.util.*

abstract class Highlighter(
    private val lexerOf: (CharStream) -> Lexer,
    private val parserOf: (CommonTokenStream) -> Parser,
    private val startRuleOf: (Parser) -> RuleContext,
    //
    private val lexicalHighlighter: LexicalHighlighter,
    private val grammaticalHighlighter: GrammaticalHighlighter
) {
    fun highlight(src: String): Array<HTok>? =
        try {
            val charStream = CharStreams.fromString(src)

            // Lexer.
            val lexer = lexerOf(charStream)
            lexer.removeErrorListeners()
            //
            val tokenStreams = CommonTokenStream(lexer)

            // Parser.
            val parser = parserOf(tokenStreams)
            parser.removeErrorListeners()
            parser.errorHandler = DefaultErrorStrategy()
            //
            val c0 = startRuleOf(parser)

            val hMap = TreeMap<Int, HTok>()

            tokenStreams.tokens.forEach { t ->
                hMap[t.startIndex] = lexicalHighlighter.hCodeOf(LTok(t))
            }
            tokenStreams.seek(0)

            grammaticalHighlighter.reset()
            ParseTreeWalker.DEFAULT.walk(grammaticalHighlighter, c0)
            grammaticalHighlighter.getOverrides().forEach {
                hMap[it.startIndex] = it
            }
            grammaticalHighlighter.reset()

            hMap.values.toTypedArray()
        } catch (ignored: Exception) {
            null
        }
}