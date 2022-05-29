package com.hack3rz.annotationservice.dto;

import com.hack3rz.annotationservice.enumeration.SupportedLanguage;
import lombok.Getter;
import lombok.Setter;

import javax.validation.constraints.NotNull;

/**
 * DTO for code annotation requests
 */

@Getter
@Setter
public class AnnotateCodeRequestDTO {

   /**
    * The source code
    */
   @NotNull
   private String code;

   /**
    * The supported languages (will automatically be cast from string values)
    */
   @NotNull
   private SupportedLanguage language;

}
