package com.hack3rz.annotationservice.controller;

import com.hack3rz.annotationservice.dto.AnnotateCodeRequestDTO;
import com.hack3rz.annotationservice.model.Annotation;
import com.hack3rz.annotationservice.repository.AnnotationRepository;
import com.hack3rz.annotationservice.service.AnnotationService;
import lexer.HTok;
import lexer.LTok;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

import java.util.Date;

import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE;

@RestController
@RequestMapping(value = "/api/annotate", produces = APPLICATION_JSON_VALUE)
public class AnnotationController {
    private static final Logger log = LoggerFactory.getLogger(AnnotationController.class);

    @Autowired
    private AnnotationService annotationService;

    @Autowired
    private AnnotationRepository repository;

    @PostMapping()
    public LTok[] annotateCode(@RequestBody @Valid AnnotateCodeRequestDTO dto) {
        log.info("Received a code annotation request for language: {}", dto.getLanguage());

        // TODO: refactor logic into service so controller stays slim

        LTok[] lexingTokens = annotationService.lexCode(dto.getCode(), dto.getLanguage());
        HTok[] highlightingTokens = annotationService.highlightCode(dto.getCode(), dto.getLanguage());

        // only for debugging purposes and to compare our solution to the java highlighter
        String htmlCode = annotationService.debugHighlightCode(dto.getCode(), dto.getLanguage());

        // Store in database
        Annotation annotation = Annotation.builder()
                .sourceCode(dto.getCode())
                .language(dto.getLanguage())
                .lexingTokes(annotationService.pluckTokenIds(lexingTokens))
                .highlightingTokens(annotationService.pluckHCodeValues(highlightingTokens))
                .highlightingCode(htmlCode)
                .timestamp(new Date())
                .build();

        repository.save(annotation);

        // TODO: if we run into performance issues we could asynchronously highlight / debug the code and return the lexing straight away

        return lexingTokens;
    }
}
