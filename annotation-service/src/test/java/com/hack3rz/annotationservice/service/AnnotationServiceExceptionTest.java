package com.hack3rz.annotationservice.service;

import com.hack3rz.annotationservice.enumeration.SupportedLanguage;
import com.hack3rz.annotationservice.exception.ApiException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.http.HttpStatus;
import org.springframework.test.context.junit4.SpringRunner;
import resolver.JavaResolver;
import resolver.Resolver;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.when;

/**
 * Test that mocks the resolver to ensure proper exception handling by the annotation service
 */
@RunWith(SpringRunner.class)
@SpringBootTest
@ComponentScan("com.hack3rz.annotationservice")
class AnnotationServiceExceptionTest {

    @Autowired
   private AnnotationService annotationService;

    @MockBean
    private JavaResolver resolver;

    private final String code =  "public static void main(String[] args) {}";

    @BeforeEach
    public void setUp() {
        // first we create a mock resolver that will always return null
        Resolver resolver = Mockito.mock(JavaResolver.class, Mockito.RETURNS_DEEP_STUBS);
        when(resolver.lex(code)).thenReturn(null);
        when(resolver.highlight(code)).thenReturn(null);
        when(resolver.debug(code)).thenReturn(null);

        // then we mock only the getResolverMethod to return our mocked resolver
        annotationService = spy(AnnotationService.class);
        when(annotationService.getResolverByLanguage(SupportedLanguage.JAVA)).thenReturn(resolver);
    }

    @Test
    void whenErrorDuringLexing_throwApiException() {
        ApiException exception = assertThrows(ApiException.class, () -> {
            annotationService.lexCode(code, SupportedLanguage.JAVA);
        });

        assertEquals(HttpStatus.BAD_REQUEST, exception.getStatus());
    }

    @Test
    void whenErrorDuringHighlighting_throwApiException() {
        ApiException exception = assertThrows(ApiException.class, () -> {
            annotationService.highlightCode(code, SupportedLanguage.JAVA);
        });

        assertEquals(HttpStatus.BAD_REQUEST, exception.getStatus());
    }

    @Test
    void whenErrorDuringDebugHighlighting_throwApiException() {
        ApiException exception = assertThrows(ApiException.class, () -> {
            annotationService.debugHighlightCode(code, SupportedLanguage.JAVA);
        });

        assertEquals(HttpStatus.BAD_REQUEST, exception.getStatus());
    }
}
