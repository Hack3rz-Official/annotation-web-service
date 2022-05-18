export enum HCodes {
  ANY,
  // Lexically identifiable.
  KEYWORD,
  LITERAL,
  CHAR_STRING_LITERAL,
  COMMENT,
  // Grammatically identifiable.
  // Declarator identifiers.
  CLASS_DECLARATOR,
  FUNCTION_DECLARATOR,
  VARIABLE_DECLARATOR,
  // Identifiers.
  TYPE_IDENTIFIER,
  FUNCTION_IDENTIFIER,
  FIELD_IDENTIFIER,
  // Annotations.
  ANNOTATION_DECLARATOR
}