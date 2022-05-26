package com.hack3rz.annotationservice.service;

import com.hack3rz.annotationservice.enumeration.SupportedLanguage;
import com.hack3rz.annotationservice.exception.ApiException;
import com.hack3rz.annotationservice.model.Annotation;
import com.hack3rz.annotationservice.repository.AnnotationRepository;
import lexer.HTok;
import lexer.LTok;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.springframework.scheduling.annotation.Async;
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
@EnableMongoRepositories
public class AnnotationService {
    private static final Logger log = LoggerFactory.getLogger(AnnotationService.class);
    private static final String INSTANTIATED_RESOLVER_OF_TYPE = "Instantiated resolver of type {}";
    private static final String COULD_NOT_BE_HIGHLIGHTED = "Code could not be highlighted.";

    @Autowired
    private AnnotationRepository repository;


    /**
     * Lexes the provided code
     * @param code the code that should be lexed
     * @param language the language of the provided code
     * @return a list of lexing tokens
     */
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

    /**
     * Highlights the provided code
     * @param code the coude that should be highlighted
     * @param language the language of the provided code
     * @return a list of highlight tokens
     */
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

    /**
     * Creates highlighted HTML code for debugging purposes
     * @param code the code to be highlighted
     * @param language the language of the provided code
     * @return highlighted HTML code
     */
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

    /**
     * Persists the annotation to the database
     * @param code the code
     * @param language the language of the code
     */
    @Async
    public void persistCode(String code, SupportedLanguage language) {
        HTok[] highlightingTokens = highlightCode(code, language);

        // only for debugging purposes and to compare our solution to the java highlighter
        String htmlCode = debugHighlightCode(code, language);

        // Store in database
        Annotation.AnnotationKey annotationKey = new Annotation.AnnotationKey(language, pluckTokenIds(highlightingTokens));
        Annotation annotation = Annotation.builder()
                .id(annotationKey)
                .sourceCode(code)
                .highlightingTokens(pluckHCodeValues(highlightingTokens))
                .highlightingCode(htmlCode)
                .build();

        repository.save(annotation);
    }


    /**
     * Plucks the token ids from a list of LToks
     * @param lToks the list of LToks
     * @return a list of token ids
     */
    public List<Integer> pluckTokenIds(LTok[] lToks) {
        return Arrays.stream(lToks).map(lTok -> lTok.tokenId).collect(Collectors.toList());
    }

    /**
     * Plucks the HCode values from a list of HToks
     * @param hToks the list of HToks
     * @return a list of HCode values
     */
    public List<Integer> pluckHCodeValues(HTok[] hToks) {
        return Arrays.stream(hToks).map(hTok -> hTok.hCodeValue).collect(Collectors.toList());
    }

    /**
     * Picks the correct resolver based on the supported language
     * @param language the language
     * @return an instance of the resolver
     */
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
