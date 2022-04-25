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
import java.util.List;
import java.util.stream.Collectors;

import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.KOTLIN;
import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.PYTHON3;
import static org.springframework.http.HttpStatus.BAD_REQUEST;

/**
 * Service for providing the lexed tokens
 */
@Service
public class AnnotationService {
    private static final Logger log = LoggerFactory.getLogger(AnnotationService.class);
    private static final String INSTANTIATED_RESOLVER_OF_TYPE = "Instantiated resolver of type {}";
    private static final String COULD_NOT_BE_HIGHLIGHTED = "Code could not be highlighted.";

    public LTok[] lexCode(String code, SupportedLanguage language) {
        log.info("Received code to annotate...");

        Resolver resolver = getResolverByLanguage(language);
        log.info(INSTANTIATED_RESOLVER_OF_TYPE, resolver.getClass());

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
        log.info(INSTANTIATED_RESOLVER_OF_TYPE, resolver.getClass());

        HTok[] highlightTokens = resolver.highlight(code);

        if (highlightTokens == null) {
            log.error(COULD_NOT_BE_HIGHLIGHTED);
            throw new ApiException(BAD_REQUEST, COULD_NOT_BE_HIGHLIGHTED, "highlightTokens was null");
        }

        log.info("HighlightToken length = {}", highlightTokens.length);

        return highlightTokens;
    }

    public String debugHighlightCode(String code, SupportedLanguage language) {
        log.info("Received code to highlight...");

        Resolver resolver = getResolverByLanguage(language);
        log.info(INSTANTIATED_RESOLVER_OF_TYPE, resolver.getClass());

        String htmlCode = resolver.debug(code);

        if (htmlCode == null) {
            log.error(COULD_NOT_BE_HIGHLIGHTED);
            throw new ApiException(BAD_REQUEST, COULD_NOT_BE_HIGHLIGHTED, "htmlCode was null");
        }

        return htmlCode;
    }

    public List<Integer> pluckTokenIds(LTok[] lToks) {
        return Arrays.stream(lToks).map(lTok -> lTok.tokenId).collect(Collectors.toList());
    }

    public List<Integer> pluckHCodeValues(HTok[] hToks) {
        return Arrays.stream(hToks).map(hTok -> hTok.hCodeValue).collect(Collectors.toList());
    }

    private Resolver getResolverByLanguage(SupportedLanguage language) {
        Resolver resolver;

        if (language == PYTHON3) {
            resolver = new Python3Resolver();
        } else if (language == KOTLIN) {
            resolver = new KotlinResolver();
        } else {
            resolver = new JavaResolver();
        }

        return resolver;
    }
}
