package com.hack3rz.annotationservice.controller;

import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE;

import javax.validation.Valid;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.hack3rz.annotationservice.dto.AnnotateCodeRequestDTO;
import com.hack3rz.annotationservice.service.AnnotationService;

@RestController
@RequestMapping(value = "/api/annotate", produces = APPLICATION_JSON_VALUE)
public class AnnotationController {
    private static final Logger log = LoggerFactory.getLogger(AnnotationController.class);

    @Autowired
    private AnnotationService annotationService;

    @PostMapping()
    public String annotateCode(@RequestBody @Valid AnnotateCodeRequestDTO dto) {
        log.info("Received a code annotation request for language: {}", dto.getLanguage());
        return annotationService.annotateCode(dto.getCode(), dto.getLanguage());
    }
}
