package com.hack3rz.annotationservice.service;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

class AnnotationServiceTest {

    /*

    private AnnotationService annotationService;

    @BeforeEach
    public void setupVariables() {
        annotationService = new AnnotationService();
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
        assertEquals(expectedLexingResult, annotationService.pluckTokenIds(annotationService.lexCode(code, PYTHON)));
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
        assertEquals(expectedLexingResult, annotationService.pluckTokenIds(annotationService.lexCode(code, PYTHON)));
    }

    @Test
    void whenJavaCodeCanNotBeLexed_thenFailGracefully() {
        String code = "\"{ emptyResult }";

        Assertions.assertTrue(annotationService.pluckTokenIds(annotationService.lexCode(code, JAVA)).isEmpty());
    }

    */
}