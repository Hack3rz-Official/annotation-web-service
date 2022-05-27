package com.hack3rz.annotationservice.controller;

import com.hack3rz.annotationservice.dto.AnnotateCodeRequestDTO;
import com.hack3rz.annotationservice.service.AnnotationService;
import lexer.LTok;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE;

/**
 * Controller that handles the annotation endpoint
 */
@RestController
@RequestMapping(value = "/api/v1/annotation", produces = APPLICATION_JSON_VALUE)
public class AnnotationController {
    private static final Logger log = LoggerFactory.getLogger(AnnotationController.class);

    @Autowired
    private AnnotationService annotationService;


    /**
     * Controller method that handles the POST request to the endpoint
     * @param dto the DataTransferObject for this endpoint
     * @return the lexing tokens (will automatically be serialized to JSON)
     */
    @PostMapping()
    public LTok[] annotateCode(@RequestBody @Valid AnnotateCodeRequestDTO dto) {
        log.info("Received a code annotation request for language: {}", dto.getLanguage());

        LTok[] lexingTokens = annotationService.lexCode(dto.getCode(), dto.getLanguage());

        // this method runs asynchronously so the method can return early
        annotationService.persistCode(dto.getCode(), dto.getLanguage());

        return lexingTokens;
    }
}
