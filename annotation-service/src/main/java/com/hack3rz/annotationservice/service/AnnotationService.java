package com.hack3rz.annotationservice.service;

import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.KOTLIN;
import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.PYTHON;
import static org.springframework.http.HttpStatus.BAD_REQUEST;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.hack3rz.annotationservice.enumeration.SupportedLanguage;
import com.hack3rz.annotationservice.exception.ApiException;

import lexer.LTok;
import resolver.KotlinResolver;
import resolver.Python3Resolver;
import resolver.Resolver;
import resolver.JavaResolver;

/**
 * Service for providing the lexed tokens
 */
@Service
public class AnnotationService {
    private static final Logger log = LoggerFactory.getLogger(AnnotationService.class);

    public LTok[] annotateCode(String code, SupportedLanguage language) {
        log.info("Received code to annotate...");

        Resolver resolver = getResolverByLanguage(language);
        log.info("Instantiated resolver of type {}", resolver.getClass());

        LTok[] lexingTokens = resolver.lex(code);

        if (lexingTokens == null) {
            log.error("Code could not be lexed.");
            throw new ApiException(BAD_REQUEST, "Code could not be lexed.", "lexingTokens was null");
        }
        return lexingTokens;
    }

    private Resolver getResolverByLanguage(SupportedLanguage language) {
        Resolver resolver;

        if (language == PYTHON) {
            resolver = new Python3Resolver();
        } else if (language == KOTLIN) {
            resolver = new KotlinResolver();
        } else {
            resolver = new JavaResolver();
        }

        return resolver;
    }
}
