package com.hack3rz.annotationservice.model;

import com.hack3rz.annotationservice.enumeration.SupportedLanguage;
import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

/**
 * Model for the annotations collection in the database
 */
@Document("annotations")
@Builder
@Getter
public class Annotation {

    @Id
    private AnnotationKey id;

    @Value
    @AllArgsConstructor
    public static class AnnotationKey {
        private SupportedLanguage language;
        private List<Integer> lexingTokens;
    }

    private String sourceCode;

    private List<Integer> highlightingTokens;

    private String highlightingCode;
}
