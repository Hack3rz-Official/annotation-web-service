package highlighter.kotlinhighlighter

import HTok
import LTok
import highlighter.LexicalHighlighter
import KotlinLexer
import HCode

class KotlinLexicalHighlighter: LexicalHighlighter(lexer.KotlinLexer()) {

    private val strongKeywords =
        hashSetOf(
            KotlinLexer.RETURN_AT, KotlinLexer.CONTINUE_AT, KotlinLexer.BREAK_AT , KotlinLexer.THIS_AT , KotlinLexer.SUPER_AT,
            KotlinLexer.PACKAGE, KotlinLexer.CLASS, KotlinLexer.INTERFACE, KotlinLexer.FUN, KotlinLexer.OBJECT, KotlinLexer.VAL,
            KotlinLexer.VAR, KotlinLexer.TYPE_ALIAS, KotlinLexer.THIS, KotlinLexer.SUPER, KotlinLexer.TYPEOF, KotlinLexer.IF,
            KotlinLexer.ELSE, KotlinLexer.WHEN, KotlinLexer.TRY, KotlinLexer.FOR, KotlinLexer.DO, KotlinLexer.WHILE, KotlinLexer.THROW,
            KotlinLexer.RETURN, KotlinLexer.CONTINUE, KotlinLexer.BREAK, KotlinLexer.AS, KotlinLexer.IS, KotlinLexer.IN,
            KotlinLexer.NOT_IS, KotlinLexer.NOT_IN
        )

    private val keywords =
        strongKeywords + softKeyworkds

    private val literals =
        hashSetOf(
            KotlinLexer.RealLiteral, KotlinLexer.FloatLiteral, KotlinLexer.DoubleLiteral, KotlinLexer.IntegerLiteral,
            KotlinLexer.HexLiteral, KotlinLexer.BinLiteral, KotlinLexer.UnsignedLiteral, KotlinLexer.LongLiteral,
            KotlinLexer.BooleanLiteral, KotlinLexer.NullLiteral
        )

    private val stringLiterals =
        hashSetOf(
            KotlinLexer.CharacterLiteral,  KotlinLexer.QUOTE_OPEN,  KotlinLexer.TRIPLE_QUOTE_OPEN,  KotlinLexer.QUOTE_CLOSE,
            KotlinLexer.LineStrRef,  KotlinLexer.LineStrText, KotlinLexer.LineStrEscapedChar,  KotlinLexer.LineStrExprStart,
            KotlinLexer.TRIPLE_QUOTE_CLOSE,  KotlinLexer.MultiLineStringQuote,  KotlinLexer.MultiLineStrRef,
            KotlinLexer.MultiLineStrText, KotlinLexer.MultiLineStrExprStart
        )

    private val comments =
        hashSetOf(
            KotlinLexer.ShebangLine, KotlinLexer.LineComment, KotlinLexer.DelimitedComment, KotlinLexer.Inside_Comment
        )

    override fun hCodeOf(lTok: LTok): HTok =
        when (lTok.tokenId) {
            in keywords -> HTok(lTok, HCode.KEYWORD)
            in literals -> HTok(lTok, HCode.LITERAL)
            in stringLiterals -> HTok(lTok, HCode.CHAR_STRING_LITERAL)
            in comments -> HTok(lTok, HCode.COMMENT)
            else -> HTok(lTok, HCode.ANY)
        }

    companion object {
        val softKeyworkds =
            hashSetOf(
                KotlinLexer.ABSTRACT, KotlinLexer.ANNOTATION, KotlinLexer.BY, KotlinLexer.CATCH, KotlinLexer.COMPANION,
                KotlinLexer.CONSTRUCTOR, KotlinLexer.CROSSINLINE, KotlinLexer.DATA, KotlinLexer.DYNAMIC, KotlinLexer.ENUM,
                KotlinLexer.EXTERNAL, KotlinLexer.FINAL, KotlinLexer.FINALLY, KotlinLexer.IMPORT, KotlinLexer.INFIX,
                KotlinLexer.INIT, KotlinLexer.INLINE, KotlinLexer.INNER, KotlinLexer.INTERNAL, KotlinLexer.LATEINIT,
                KotlinLexer.NOINLINE, KotlinLexer.OPEN, KotlinLexer.OPERATOR, KotlinLexer.OUT, KotlinLexer.OVERRIDE,
                KotlinLexer.PRIVATE, KotlinLexer.PROTECTED, KotlinLexer.PUBLIC, KotlinLexer.REIFIED, KotlinLexer.SEALED,
                KotlinLexer.TAILREC, KotlinLexer.VARARG, KotlinLexer.WHERE, KotlinLexer.GET, KotlinLexer.SET, KotlinLexer.FIELD,
                KotlinLexer.PROPERTY, KotlinLexer.RECEIVER, KotlinLexer.PARAM, KotlinLexer.SETPARAM, KotlinLexer.DELEGATE,
                KotlinLexer.FILE, KotlinLexer.EXPECT, KotlinLexer.ACTUAL, KotlinLexer.VALUE, KotlinLexer.CONST, KotlinLexer.SUSPEND
            )
    }
}
