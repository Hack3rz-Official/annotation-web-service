import org.antlr.v4.runtime.Token;

/**
 * Represents the lexical positioning and identity of a token.
 */
public class LTok {
    /**
     * Char index position in text where the first charchter
     * in the token's text is found.
     */
    public final int startIndex;

    /**
     * Char index position in text where the last charchter
     * in the token's text is found.
     */
    public final int endIndex;

    /**
     * Token integer identifier as specified in the lexer vocabulary.
     */
    public final int tokenId;

    public LTok(int startIndex, int endIndex, int tokenId) {
        this.startIndex = startIndex;
        this.endIndex = endIndex;
        this.tokenId = tokenId;
    }

    public LTok(Token token) {
        this(token.getStartIndex(), token.getStopIndex(), token.getType());
    }

    @Override
    public String toString() {
        return "LTok{" +
                "startIndex=" + startIndex +
                ", endIndex=" + endIndex +
                ", tokenId=" + tokenId +
                '}';
    }
}
