package com.hack3rz.annotationservice.service;

import com.hack3rz.annotationservice.repository.AnnotationRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.util.Arrays;
import java.util.List;

import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

@DataMongoTest
@ComponentScan("com.hack3rz.annotationservice")
@ExtendWith(SpringExtension.class)
@ActiveProfiles(profiles = "test")
class AnnotationServiceTest {

    @Autowired
    private AnnotationService annotationService;

    @Autowired
    MongoTemplate mongoTemplate;

    @AfterEach
    void afterEach() {
        mongoTemplate.getDb().drop();
    }

    @Test
    void whenValidJavaCode_thenReturnLexedTokens() {
        String code = "public static void main(String[] args) {}";
        List<Integer> expectedLexingResult = Arrays.asList(35, 38, 48, 102, 57, 102, 61, 62, 102, 58, 59, 60);

        assertEquals(expectedLexingResult, annotationService.pluckTokenIds(annotationService.lexCode(code, JAVA)));
    }

    @Test
    void whenValidKotlinCode_thenReturnLexedTokens() {
        String code = "fun main() { println(\"Hello, World!\") }";
        List<Integer> expectedLexingResult = Arrays.asList(74, 4, 146, 9, 10, 4, 13, 4, 146, 9, 149, 160, 158, 10, 4, 14);
        assertEquals(expectedLexingResult, annotationService.pluckTokenIds(annotationService.lexCode(code, KOTLIN)));
    }

    @Test
    void whenValidPython3Code_thenReturnLexedTokens() {
        String code = "print(\"Hello World\")";
        List<Integer> expectedLexingResult = Arrays.asList(42, 54, 3, 55);
        assertEquals(expectedLexingResult, annotationService.pluckTokenIds(annotationService.lexCode(code, PYTHON3)));
    }

    @Test
    void whenIncompleteJavaCode_thenReturnLexedTokens() {
        String code = "public static void mai}";
        List<Integer> expectedLexingResult = Arrays.asList(35, 38, 48, 102, 60);
        assertEquals(expectedLexingResult, annotationService.pluckTokenIds(annotationService.lexCode(code, JAVA)));
    }

    @Test
    void whenIncompleteKotlinCode_thenReturnLexedTokens() {
        String code = "fun main() {";
        List<Integer> expectedLexingResult = Arrays.asList(74, 4, 146, 9, 10, 4, 13);
        assertEquals(expectedLexingResult, annotationService.pluckTokenIds(annotationService.lexCode(code, KOTLIN)));
    }

    @Test
    void whenIncompletePython3Code_thenReturnLexedTokens() {
        String code = "print(";
        List<Integer> expectedLexingResult = Arrays.asList(42, 54);
        assertEquals(expectedLexingResult, annotationService.pluckTokenIds(annotationService.lexCode(code, PYTHON3)));
    }

    @Test
    void whenJavaCodeCanNotBeLexed_thenFailGracefully() {
        String code = "\"{ emptyResult }";

        Assertions.assertTrue(annotationService.pluckTokenIds(annotationService.lexCode(code, JAVA)).isEmpty());
    }

    @Test
    void whenValidJavaCode_thenReturnHighlightTokens() {
        String code = "public static void main(String[] args) {}";
        List<Integer> expectedHighlightResult = Arrays.asList(35, 38, 48, 102, 57, 102, 61, 62, 102, 58, 59, 60, -1);

        assertEquals(expectedHighlightResult, annotationService.pluckTokenIds(annotationService.highlightCode(code, JAVA)));
    }

    @Test
    void whenValidKotlinCode_thenReturnHighlightTokens() {
        String code = "fun main() { println(\"Hello, World!\") }";
        List<Integer> expectedHighlightResult = Arrays.asList(74, 4, 146, 9, 10, 4, 13, 4, 146, 9, 149, 160, 158, 10, 4, 14, -1);
        assertEquals(expectedHighlightResult, annotationService.pluckTokenIds(annotationService.highlightCode(code, KOTLIN)));
    }

    @Test
    void whenValidPython3Code_thenReturnHighlightTokens() {
        String code = "print(\"Hello World\")";
        List<Integer> expectedHighlightResult = Arrays.asList(42, 54, 3, 55, -1);
        assertEquals(expectedHighlightResult, annotationService.pluckTokenIds(annotationService.highlightCode(code, PYTHON3)));
    }

    @Test
    void whenValidJavaCode_thenReturnHighlightHTMLCode() {
        String code = "public static void main(String[] args) {}";
        String expectedHighlightResult = "<code class=\"KEYWORD\">public</code> <code class=\"KEYWORD\">static</code> <code class=\"KEYWORD\">void</code> <code class=\"ANY\">main</code><code class=\"ANY\">(</code><code class=\"ANY\">String</code><code class=\"ANY\">[</code><code class=\"ANY\">]</code> <code class=\"ANY\">args</code><code class=\"ANY\">)</code> <code class=\"ANY\">{</code><code class=\"ANY\">}</code>";
        String highlightedCode = annotationService.debugHighlightCode(code, JAVA);
        Assertions.assertTrue(highlightedCode.contains(expectedHighlightResult));
    }

    @Test
    void whenValidKotlinCode_thenReturnHighlightHTMLCode() {
        String code = "fun main() { println(\"Hello, World!\") }";
        String expectedHighlightResult = "<code class=\"KEYWORD\">fun</code><code class=\"ANY\"> </code><code class=\"FUNCTION_DECLARATOR\">main</code><code class=\"ANY\">(</code><code class=\"ANY\">)</code><code class=\"ANY\"> </code><code class=\"ANY\">{</code><code class=\"ANY\"> </code><code class=\"FUNCTION_IDENTIFIER\">println</code><code class=\"ANY\">(</code><code class=\"CHAR_STRING_LITERAL\">\"</code><code class=\"CHAR_STRING_LITERAL\">Hello, World!</code><code class=\"CHAR_STRING_LITERAL\">\"</code><code class=\"ANY\">)</code><code class=\"ANY\"> </code><code class=\"ANY\">}</code>";
        String highlightedCode = annotationService.debugHighlightCode(code, KOTLIN);
        Assertions.assertTrue(highlightedCode.contains(expectedHighlightResult));
    }

    @Test
    void whenValidPython3Code_thenReturnHighlightHTMLCode() {
        String code = "print(\"Hello World\")";
        String expectedHighlightResult = "<code class=\"FUNCTION_IDENTIFIER\">print</code><code class=\"ANY\">(</code><code class=\"CHAR_STRING_LITERAL\">\"Hello World\"</code><code class=\"ANY\">)</code>";
        Assertions.assertTrue(annotationService.debugHighlightCode(code, PYTHON3).contains(expectedHighlightResult));
    }

    @Test
    void persistAnnotationToDatabase(@Autowired AnnotationRepository repository) {
        String code = "public static void main(String[] args) {}";
        annotationService.persistCode(code, JAVA);
        Assertions.assertTrue(repository.existsAnnotationBySourceCode(code));
    }

}