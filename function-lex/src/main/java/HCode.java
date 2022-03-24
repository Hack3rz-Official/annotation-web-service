public enum HCode {
    ANY(0),
    // Lexically identifiable.
    KEYWORD(1),
    LITERAL(2),
    CHAR_STRING_LITERAL(3),
    COMMENT(4),
    //
    // Grammatically identifiable.
    // Declarator identifiers.
    CLASS_DECLARATOR(5),
    FUNCTION_DECLARATOR(6),
    VARIABLE_DECLARATOR(7),
    // Identifiers.
    TYPE_IDENTIFIER(8),
    FUNCTION_IDENTIFIER(9),
    FIELD_IDENTIFIER(10),
    // Annotations.
    ANNOTATION_DECLARATOR(11);

    public final int hCodeValue;
    HCode(int hCodeValue) {
        this.hCodeValue = hCodeValue;
    }

    @Override
    public String toString() {
        return "HCode{" +
                "name=" + this.name() +
                ", hCodeValue=" + hCodeValue +
                '}';
    }
}
