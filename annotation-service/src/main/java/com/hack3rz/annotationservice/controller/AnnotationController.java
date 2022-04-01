package com.hack3rz.annotationservice.controller;

import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE;

import javax.validation.Valid;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.hack3rz.annotationservice.dto.AnnotateCodeRequestDTO;

@RestController
@RequestMapping(value = "/api/annotate", produces = APPLICATION_JSON_VALUE)
public class AnnotationController {
    private static final Logger log = LoggerFactory.getLogger(AnnotationController.class);

    @PostMapping()
    public void annotateCode(@RequestBody @Valid AnnotateCodeRequestDTO dto) {
        log.info("Received a code annotation request for language: {}", dto.getLanguage());
    }

}
