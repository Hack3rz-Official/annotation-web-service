package com.hack3rz.annotationservice.model;

import com.hack3rz.annotationservice.enumeration.SupportedLanguage;
import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;
import java.util.List;

@Getter
@Setter
@Document("annotations")
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Annotation {

    @Id
    private String id;

    private String sourceCode;
    private List<Integer> lexingTokes;
    private List<Integer> highlightingTokens;

    private String highlightingCode;

    private Date timestamp;

    private SupportedLanguage language;

}
