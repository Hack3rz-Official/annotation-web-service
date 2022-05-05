package com.functions.dtos;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.functions.SupportedLanguage;

public class LexRequestDTO {

    @JsonProperty("code")
    private String code;

    @JsonProperty("lang_name")
    private SupportedLanguage language;

    // empty constructor is needed for jackson deserialization
    public LexRequestDTO() {}

    public LexRequestDTO(String code, SupportedLanguage language) {
        this.code = code;
        this.language = language;
    }

    public SupportedLanguage getLanguage() {
        return language;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public void setLanguage(SupportedLanguage language) {
        this.language = language;
    }

}
