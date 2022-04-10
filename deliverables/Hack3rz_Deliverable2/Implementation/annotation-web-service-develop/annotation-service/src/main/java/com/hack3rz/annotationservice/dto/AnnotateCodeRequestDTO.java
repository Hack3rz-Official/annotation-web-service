package com.hack3rz.annotationservice.dto;

import javax.validation.constraints.NotNull;

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
   private SupportedLanguage language;

}
