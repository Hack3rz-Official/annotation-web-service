import org.antlr.v4.runtime.Token;

/**
 * Represents the lexical positioning, identity, and highlighting value of a token.
 */
public class HTok extends LTok {

    /**
     * Represents the highlighting code value as indicated in
     * the reference highlighting table.
     */
    public final int hCodeValue;

    public HTok(int startIndex, int endIndex, int tokenId, int hCodeValue) {
        super(startIndex, endIndex, tokenId);
        this.hCodeValue = hCodeValue;
    }

    public HTok(Token token, HCode hCode) {
        super(token);
        this.hCodeValue = hCode.hCodeValue;
    }

    public HTok(LTok lTok, int hCodeValue) {
        this(lTok.startIndex, lTok.endIndex, lTok.tokenId, hCodeValue);
    }

    public HTok(LTok lTok, HCode hCode) {
        this(lTok, hCode.hCodeValue);
    }

    @Override
    public String toString() {
        return "HTok{" +
                "hCodeValue=" + hCodeValue +
                ", startIndex=" + startIndex +
                ", endIndex=" + endIndex +
                ", tokenId=" + tokenId +
                '}';
    }
}
