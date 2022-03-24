import org.antlr.v4.runtime.ParserRuleContext
import org.antlr.v4.runtime.tree.ParseTree
import org.antlr.v4.runtime.tree.TerminalNode
import java.util.*

fun ParseTree?.isTerminal(): TerminalNode? =
    if (this != null && this is TerminalNode) this else null


fun ParseTree?.isTerminal(ruleIndex: Int?): TerminalNode? =
    if (ruleIndex == null)
        this.isTerminal()
    else
        this.isTerminal()?.let {
            if (it.symbol.type == ruleIndex) it else null
        }

fun ParseTree?.isTerminal(ruleIndexes: Set<Int>?): TerminalNode? =
    if (ruleIndexes == null)
        this.isTerminal()
    else
        this.isTerminal()?.let {
            if (ruleIndexes.contains(it.symbol.type)) it else null
        }

fun ParseTree?.isProduction(): ParserRuleContext? =
    if (this != null && this is ParserRuleContext) this else null

fun ParseTree?.isProduction(ruleIndex: Int?): ParserRuleContext? =
    if (ruleIndex == null)
        this.isProduction()
    else
        this.isProduction()?.let {
            if (it.ruleIndex == ruleIndex) it else null
        }

fun ParseTree?.isProduction(ruleIndexes: Set<Int>?): ParserRuleContext? =
    if (ruleIndexes == null)
        this.isProduction()
    else
        this.isProduction()?.let {
            if (ruleIndexes.contains(it.ruleIndex)) it else null
        }

fun ParserRuleContext.innerHToks(hCode: HCode): List<HTok> {
    val hToks = LinkedList<HTok>()

    val fringe = LinkedList<ParseTree>()
    fringe.add(this)
    while (fringe.isNotEmpty())
        fringe.pop().let { prc ->
            prc.isTerminal()?.let { hToks.add(HTok(it.symbol, hCode)) } ?:
            prc.isProduction()?.children?.map { fringe.addLast(it) }
        }

    return hToks
}

fun ParserRuleContext?.loopingOnChildren(
    addReplacingFunc: (HTok) -> Unit,
    onTerminal: (TerminalNode) -> HCode? = { _ -> null },
    targetTerminalIndex: Int? = null,
    onProduction: (ParserRuleContext) -> HCode? = { _ -> null },
    targetProductionIndex: Int? = null,
    onAddedExit: Boolean = false,
    reversed: Boolean = false,
) {
    val mpts = if (reversed) this?.children?.reversed() else this?.children
    if (mpts != null)
        for (mpt in mpts) {
            val mHToks =
                mpt.isTerminal(targetTerminalIndex)?.let { t -> onTerminal(t)?.let { hc -> listOf(HTok(t.symbol, hc)) } }
                    ?: mpt.isProduction(targetProductionIndex)?.let { p -> onProduction(p)?.let { hc -> p.innerHToks(hc) } }
            //
            mHToks?.let { hToks ->
                hToks.forEach(addReplacingFunc)
                if (onAddedExit)
                    return
            }
        }
}
