package com.functions;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Enum that defines the supported languages of the lexing function
 */
public enum SupportedLanguage {
    @JsonProperty("java") JAVA,
    @JsonProperty("kotlin") KOTLIN,
    @JsonProperty("python") PYTHON;
}
