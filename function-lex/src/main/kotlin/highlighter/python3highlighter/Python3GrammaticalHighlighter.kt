package highlighter.python3highlighter

import HCode
import HTok
import Python3ParserBaseListener
import highlighter.GrammaticalHighlighter
import innerHToks
import isProduction
import isTerminal
import loopingOnChildren
import org.antlr.v4.runtime.ParserRuleContext
import org.antlr.v4.runtime.tree.ParseTree
import org.antlr.v4.runtime.tree.TerminalNode
import java.util.*

class Python3GrammaticalHighlighter: Python3ParserBaseListener(), GrammaticalHighlighter {
    private val hToks = hashMapOf<Int, HTok>()

    private fun HTok.addReplacing() {
        hToks[this.startIndex] = this
    }

    override fun getOverrides(): Collection<HTok> =
        this.hToks.values

    override fun reset() {
        hToks.clear()
    }

    private fun ParserRuleContext?.myLoopingOnChildren(
        onTerminal: (TerminalNode) -> HCode? = { _ -> null },
        targetTerminalIndex: Int? = null,
        onProduction: (ParserRuleContext) -> HCode? = { _ -> null },
        targetProductionIndex: Int? = null,
        onAddedExit: Boolean = false,
        reversed: Boolean = false,
    ) =
        this.loopingOnChildren(
            addReplacingFunc = { it.addReplacing() },
            onTerminal = onTerminal,
            targetTerminalIndex = targetTerminalIndex,
            onProduction = onProduction,
            targetProductionIndex = targetProductionIndex,
            onAddedExit = onAddedExit,
            reversed = reversed
        )

    override fun exitClassdef(ctx: Python3Parser.ClassdefContext?) =
        ctx.myLoopingOnChildren(
            targetTerminalIndex = Python3Lexer.NAME,
            onTerminal = { HCode.CLASS_DECLARATOR },
            onAddedExit = true
        )

    override fun exitFuncdef(ctx: Python3Parser.FuncdefContext?) {
        ctx.myLoopingOnChildren(
            targetTerminalIndex = Python3Lexer.NAME,
            onTerminal = { HCode.FUNCTION_DECLARATOR },
            onAddedExit = true
        )
        ctx?.children?.getOrNull(4)?.isProduction(Python3Parser.RULE_test)?.let { typeTree ->
            typeTree.allSubNAMEStoUnit {
                HTok(it.symbol, HCode.TYPE_IDENTIFIER).addReplacing()
            }
        }
    }

    override fun exitAtom_expr(ctx: Python3Parser.Atom_exprContext?) {
        val stack = Stack<Pair<ParseTree, HCode?>?>()
        ctx.myLoopingOnChildren(
            onAddedExit = false,
            onProduction = { p ->
                p.isProduction(Python3Parser.RULE_atom)?.let { ra ->
                    ra.children[0].isTerminal(Python3Lexer.NAME)?.let { n ->
                        stack.push(Pair(n, null))
                    }
                } ?:
                p.isProduction(Python3Parser.RULE_trailer)?.let { rt ->
                    rt.children[0].isTerminal(Python3Lexer.OPEN_PAREN)?.let { _ ->
                        // Previous identifier is a function call.
                        stack.pop()?.let { li ->
                            stack.push(li.copy(second = HCode.FUNCTION_IDENTIFIER))
                        }
                        // Prevent this to ever change.
                        stack.push(null)
                    } ?:
                    rt.children[0].isTerminal(Python3Lexer.OPEN_BRACK)?.let { _ ->
                        // Previous identifier is an array identifier: prevent previous from switching.
                        stack.push(null)
                    } ?:
                    rt.children[0].isTerminal(Python3Lexer.DOT)?.let { _ ->
                        rt.children[1].isTerminal(Python3Lexer.NAME)?.let { n ->
                            // New candidate.
                            stack.push(Pair(n, HCode.FIELD_IDENTIFIER))
                        }
                    }
                }
                null
            }
        )
        stack.forEach {
            it?.let { t ->
                if (t.second != null)
                    t.first.isTerminal()?.let { p ->
                        HTok(p.symbol, t.second).addReplacing()
                    } ?:
                    t.first.isProduction()?.let { p ->
                        p.innerHToks(t.second ?: HCode.ANY).forEach{ hTok -> hTok.addReplacing() }
                    }
            }
        }
    }

    override fun exitDecorator(ctx: Python3Parser.DecoratorContext?) =
        ctx.myLoopingOnChildren(
            targetTerminalIndex = Python3Lexer.AT,
            onTerminal = { HCode.ANNOTATION_DECLARATOR },
            onProduction = {
                it.isProduction(Python3Parser.RULE_dotted_name)?.let { dn ->
                    dn.myLoopingOnChildren(
                        targetTerminalIndex = Python3Lexer.NAME,
                        onTerminal = { HCode.ANNOTATION_DECLARATOR },
                        onAddedExit = false
                    )
                }
                null
            },
            onAddedExit = false
        )

    private fun ParseTree.allSubNAMEStoUnit(action: (TerminalNode) -> Unit) {
        val fringe = Stack<ParseTree>()
        fringe.push(this)
        while(!fringe.isEmpty()) {
            val pt = fringe.pop()
            pt.isTerminal(Python3Lexer.NAME)?.let { action(it) } ?:
            pt.isProduction()?.let { p -> p.children.forEach { fringe.push(it) } }
        }
    }

    override fun exitTfpdef(ctx: Python3Parser.TfpdefContext?) {
        ctx?.children?.getOrNull(2)?.allSubNAMEStoUnit {
            HTok(it.symbol, HCode.TYPE_IDENTIFIER).addReplacing()
        }
    }

    override fun exitAnnassign(ctx: Python3Parser.AnnassignContext?) {
        ctx?.children?.getOrNull(1)?.allSubNAMEStoUnit {
            HTok(it.symbol, HCode.TYPE_IDENTIFIER).addReplacing()
        }
    }

}
