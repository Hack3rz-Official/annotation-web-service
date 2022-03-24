package highlighter.kotlinhighlighter

import HCode
import HTok
import KotlinParserBaseListener
import highlighter.GrammaticalHighlighter
import innerHToks
import isProduction
import isTerminal
import loopingOnChildren
import org.antlr.v4.runtime.ParserRuleContext
import org.antlr.v4.runtime.tree.TerminalNode
import java.util.*

class KotlinGrammaticalHighlighter: KotlinParserBaseListener(), GrammaticalHighlighter {

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

    private fun overrideSimpleUserTypeWithTargetCode(ctx: ParserRuleContext?, targetHCode: HCode) =
        ctx.myLoopingOnChildren(
            targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
            onProduction = { targetHCode },
            onAddedExit = true
        )

    override fun exitClassDeclaration(ctx: KotlinParser.ClassDeclarationContext?) {
        var isFunDeclaration = false // If false then this is a class or interface declaration.
        ctx.myLoopingOnChildren(
            onTerminal = { isFunDeclaration = true; null },
            targetTerminalIndex = KotlinLexer.FUN,
            onProduction = { if (isFunDeclaration) HCode.FUNCTION_DECLARATOR else HCode.CLASS_DECLARATOR },
            targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
            onAddedExit = true
        )
    }

    override fun exitCompanionObject(ctx: KotlinParser.CompanionObjectContext?) =
        ctx.myLoopingOnChildren(
            targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
            onProduction = { HCode.CLASS_DECLARATOR },
            onAddedExit = true
        )

    override fun exitObjectDeclaration(ctx: KotlinParser.ObjectDeclarationContext?) =
        ctx.myLoopingOnChildren(
            targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
            onProduction = { HCode.CLASS_DECLARATOR },
            onAddedExit = true
        )

    override fun exitFunctionDeclaration(ctx: KotlinParser.FunctionDeclarationContext?) =
        ctx.myLoopingOnChildren(
            targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
            onProduction = { HCode.FUNCTION_DECLARATOR },
            onAddedExit = true
        )

    override fun exitLambdaLiteral(ctx: KotlinParser.LambdaLiteralContext?) {
        ctx?.children?.get(0)?.isTerminal(KotlinLexer.LCURL)?.let {
            HTok(it.symbol, HCode.FUNCTION_DECLARATOR).addReplacing()
        }
        ctx?.children?.get(ctx.childCount - 1)?.isTerminal(KotlinLexer.RCURL)?.let {
            HTok(it.symbol, HCode.FUNCTION_DECLARATOR).addReplacing()
        }
    }

    override fun exitTypeAlias(ctx: KotlinParser.TypeAliasContext?) =
        ctx.myLoopingOnChildren(
            targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
            onProduction = { HCode.CLASS_DECLARATOR },
            onAddedExit = true
        )

    override fun exitVariableDeclaration(ctx: KotlinParser.VariableDeclarationContext?) =
        ctx.myLoopingOnChildren(
            targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
            onProduction = { HCode.VARIABLE_DECLARATOR },
            onAddedExit = true
        )

    override fun exitEnumEntry(ctx: KotlinParser.EnumEntryContext?) {
        ctx.myLoopingOnChildren(
            targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
            onProduction = { HCode.CLASS_DECLARATOR },
            onAddedExit = true
        )
    }

    override fun exitSimpleUserType(ctx: KotlinParser.SimpleUserTypeContext?) =
        overrideSimpleUserTypeWithTargetCode(ctx, HCode.TYPE_IDENTIFIER)

    override fun exitNullableType(ctx: KotlinParser.NullableTypeContext?) =
        ctx.myLoopingOnChildren(
            targetProductionIndex = KotlinParser.RULE_quest,
            onProduction = { HCode.TYPE_IDENTIFIER },
            onAddedExit = false
        )

    override fun exitPostfixUnaryExpression(ctx: KotlinParser.PostfixUnaryExpressionContext?) {
        val stack = Stack<Pair<ParserRuleContext, HCode?>>()
        ctx.myLoopingOnChildren(
            onAddedExit = false,
            onProduction = { p ->
                p.isProduction(KotlinParser.RULE_primaryExpression)?.let { stack.push(Pair(it, null)) } ?:
                p.isProduction(KotlinParser.RULE_postfixUnarySuffix)?.children?.get(0)?.let { pusc ->
                    pusc.isProduction(KotlinParser.RULE_typeArguments)?.let { _ ->
                        stack.push(stack.pop().copy(second = HCode.TYPE_IDENTIFIER)) // class_type<...>
                        // Skip rule.
                    } ?:
                    pusc.isProduction(KotlinParser.RULE_callSuffix)?.let { _ ->
                        stack.push(stack.pop().copy(second = HCode.FUNCTION_IDENTIFIER))
                        // Skip rule.
                    } ?:
                    pusc.isProduction(KotlinParser.RULE_navigationSuffix)?.let { ns ->
                        ns.myLoopingOnChildren(
                            targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
                            onProduction = { nssi ->
                                stack.push(Pair(nssi, HCode.FIELD_IDENTIFIER))
                                null
                            }
                        )
                    }
                }
                null
            }
        )
        stack.forEach {
            it.second?.let { hCode ->
                it.first.isTerminal()?.let { t -> HTok(t.symbol, hCode).addReplacing() } ?:
                it.first.isProduction()?.let { p -> p.innerHToks(hCode).forEach { ht -> ht.addReplacing() } }
            }
        }
    }

    override fun exitAssignableSuffix(ctx: KotlinParser.AssignableSuffixContext?) =
        ctx.myLoopingOnChildren(
            targetProductionIndex = KotlinParser.RULE_navigationSuffix,
            onProduction = { p ->
                p.myLoopingOnChildren(
                    targetProductionIndex = KotlinParser.RULE_simpleIdentifier,
                    onProduction = { HCode.FIELD_IDENTIFIER }
                )
                null
            }
        )

    override fun exitSingleAnnotation(ctx: KotlinParser.SingleAnnotationContext?) {
        if (ctx != null)
            for (c in ctx.children)
                if (c?.isProduction(KotlinParser.RULE_unescapedAnnotation) != null)
                    return
                else
                    c.isProduction()?.let { it.innerHToks(HCode.ANNOTATION_DECLARATOR).forEach { ht -> ht.addReplacing() } } ?:
                    c.isTerminal()?.let { HTok(it.symbol, HCode.ANNOTATION_DECLARATOR).addReplacing() }
    }

    override fun exitMultiAnnotation(ctx: KotlinParser.MultiAnnotationContext?) {
        if (ctx != null)
            for (c in ctx.children)
                if (c?.isTerminal(KotlinLexer.LSQUARE) != null)
                    return
                else
                    c.isProduction()?.let { it.innerHToks(HCode.ANNOTATION_DECLARATOR).forEach { ht -> ht.addReplacing() } } ?:
                    c.isTerminal()?.let { HTok(it.symbol, HCode.ANNOTATION_DECLARATOR).addReplacing() }
    }

    override fun exitUnescapedAnnotation(ctx: KotlinParser.UnescapedAnnotationContext?) =
        ctx.myLoopingOnChildren(
            onProduction = { p ->
                p.isProduction(KotlinParser.RULE_userType)?.let { ut ->
                    ut.myLoopingOnChildren(
                        targetProductionIndex = KotlinParser.RULE_simpleUserType,
                        onProduction = { overrideSimpleUserTypeWithTargetCode(it, HCode.ANNOTATION_DECLARATOR); null }
                    )
                } ?:
                p.isProduction(KotlinParser.RULE_constructorInvocation)?.let { ci ->
                    ci.myLoopingOnChildren(
                        targetProductionIndex = KotlinParser.RULE_userType,
                        onProduction = { ut ->
                            ut.myLoopingOnChildren(
                                targetProductionIndex = KotlinParser.RULE_simpleUserType,
                                onProduction = { overrideSimpleUserTypeWithTargetCode(it, HCode.ANNOTATION_DECLARATOR); null }
                            )
                            null
                        }
                    )
                }
                null
            }
        )

    override fun exitSimpleIdentifier(ctx: KotlinParser.SimpleIdentifierContext?) {
        ctx?.children?.getOrNull(0)?.isTerminal(KotlinLexicalHighlighter.softKeyworkds)?.let { t ->
            HTok(t.symbol, HCode.ANY).addReplacing()
        }
    }
}
