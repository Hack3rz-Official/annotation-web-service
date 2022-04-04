package com.hack3rz.annotationservice.dto;

import javax.validation.constraints.NotNull;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.hack3rz.annotationservice.enumeration.SupportedLanguage;

import lombok.Getter;
import lombok.Setter;

/**
 * DTO for code annotation requests
 */

@Getter
@Setter
public class AnnotateCodeRequestDTO {

   @NotNull
   private String code;

   @NotNull
   @JsonProperty("lang_name")
   private SupportedLanguage language;

}
