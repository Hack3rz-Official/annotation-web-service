package com.hack3rz.annotationservice.service;

import com.hack3rz.annotationservice.enumeration.SupportedLanguage;
import com.hack3rz.annotationservice.exception.ApiException;
import lexer.HTok;
import lexer.LTok;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import resolver.JavaResolver;
import resolver.KotlinResolver;
import resolver.Python3Resolver;
import resolver.Resolver;

import java.util.Arrays;
import java.util.stream.Collectors;

import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.KOTLIN;
import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.PYTHON;
import static org.springframework.http.HttpStatus.BAD_REQUEST;

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

        log.info("LexingToken length = {}", lexingTokens.length);

        return lexingTokens;
    }

    public HTok[] highlightCode(String code, SupportedLanguage language) {
        log.info("Received code to highlight...");

        Resolver resolver = getResolverByLanguage(language);
        log.info("Instantiated resolver of type {}", resolver.getClass());

        HTok[] highlightTokens = resolver.highlight(code);

        if (highlightTokens == null) {
            log.error("Code could not be highlighted.");
            throw new ApiException(BAD_REQUEST, "Code could not be highlighted.", "highlightTokens was null");
        }

        log.info("HighlightToken length = {}", highlightTokens.length);
        
        return highlightTokens;
    }

    public String debugHighlightCode(String code, SupportedLanguage language) {
        log.info("Received code to highlight...");

        Resolver resolver = getResolverByLanguage(language);
        log.info("Instantiated resolver of type {}", resolver.getClass());

        String htmlCode = resolver.debug(code);

        if (htmlCode == null) {
            log.error("Code could not be highlighted.");
            throw new ApiException(BAD_REQUEST, "Code could not be highlighted.", "htmlCode was null");
        }

        return htmlCode;
    }

    public String serializeLexingTokens(LTok[] lToks) {
        return Arrays.stream(lToks).map(this::mapLTok).collect(Collectors.joining(", "));
    }

    public String serializeHighlightTokens(HTok[] hToks) {
        // TODO: check appropriate format for it
        return Arrays.stream(hToks).map(this::mapLTok).collect(Collectors.joining(", "));
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

    private String mapLTok(LTok t) {
        return "{ startIndex=" + t.startIndex + ", endIndex=" + t.endIndex + ", tokenId=" + t.tokenId + " }";
    }
}
