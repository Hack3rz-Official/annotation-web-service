package com.hack3rz.annotationservice.service;

import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.JAVA;
import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.KOTLIN;
import static com.hack3rz.annotationservice.enumeration.SupportedLanguage.PYTHON;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class AnnotationServiceTest {

    private AnnotationService annotationService;

    @BeforeEach
    public void setupVariables() {
        annotationService = new AnnotationService();
    }

    @Test
    void whenValidJavaCode_thenReturnLexedTokens() {
        String code = "public static void main(String[] args) {}";
        String expectedLexingResult = "{ startIndex=0, endIndex=5, tokenId=35 }, { startIndex=7, endIndex=12, tokenId=38 }, { startIndex=14, endIndex=17, tokenId=48 }, { startIndex=19, endIndex=22, tokenId=102 }, { startIndex=23, endIndex=23, tokenId=57 }, { startIndex=24, endIndex=29, tokenId=102 }, { startIndex=30, endIndex=30, tokenId=61 }, { startIndex=31, endIndex=31, tokenId=62 }, { startIndex=33, endIndex=36, tokenId=102 }, { startIndex=37, endIndex=37, tokenId=58 }, { startIndex=39, endIndex=39, tokenId=59 }, { startIndex=40, endIndex=40, tokenId=60 }";

        assertEquals(expectedLexingResult, annotationService.annotateCode(code, JAVA));
    }

    @Test
    void whenValidKotlinCode_thenReturnLexedTokens() {
        String code = "fun main() { println(\"Hello, World!\") }";
        String expectedLexingResult = "{ startIndex=0, endIndex=2, tokenId=74 }, { startIndex=3, endIndex=3, tokenId=4 }, { startIndex=4, endIndex=7, tokenId=146 }, { startIndex=8, endIndex=8, tokenId=9 }, { startIndex=9, endIndex=9, tokenId=10 }, { startIndex=10, endIndex=10, tokenId=4 }, { startIndex=11, endIndex=11, tokenId=13 }, { startIndex=12, endIndex=12, tokenId=4 }, { startIndex=13, endIndex=19, tokenId=146 }, { startIndex=20, endIndex=20, tokenId=9 }, { startIndex=21, endIndex=21, tokenId=149 }, { startIndex=22, endIndex=34, tokenId=160 }, { startIndex=35, endIndex=35, tokenId=158 }, { startIndex=36, endIndex=36, tokenId=10 }, { startIndex=37, endIndex=37, tokenId=4 }, { startIndex=38, endIndex=38, tokenId=14 }";

        assertEquals(expectedLexingResult, annotationService.annotateCode(code, KOTLIN));
    }

    @Test
    void whenValidPython3Code_thenReturnLexedTokens() {
        String code = "print(\"Hello World\")";
        String expectedLexingResult = "{ startIndex=0, endIndex=4, tokenId=42 }, { startIndex=5, endIndex=5, tokenId=54 }, { startIndex=6, endIndex=18, tokenId=3 }, { startIndex=19, endIndex=19, tokenId=55 }";

        assertEquals(expectedLexingResult, annotationService.annotateCode(code, PYTHON));
    }

    @Test
    void whenIncompleteJavaCode_thenReturnLexedTokens() {
        String code = "public static void mai}";
        String expectedLexingResult = "{ startIndex=0, endIndex=5, tokenId=35 }, { startIndex=7, endIndex=12, tokenId=38 }, { startIndex=14, endIndex=17, tokenId=48 }, { startIndex=19, endIndex=21, tokenId=102 }, { startIndex=22, endIndex=22, tokenId=60 }";

        assertEquals(expectedLexingResult, annotationService.annotateCode(code, JAVA));
    }

    @Test
    void whenIncompleteKotlinCode_thenReturnLexedTokens() {
        String code = "fun main() {";
        String expectedLexingResult = "{ startIndex=0, endIndex=2, tokenId=74 }, { startIndex=3, endIndex=3, tokenId=4 }, { startIndex=4, endIndex=7, tokenId=146 }, { startIndex=8, endIndex=8, tokenId=9 }, { startIndex=9, endIndex=9, tokenId=10 }, { startIndex=10, endIndex=10, tokenId=4 }, { startIndex=11, endIndex=11, tokenId=13 }";

        assertEquals(expectedLexingResult, annotationService.annotateCode(code, KOTLIN));
    }

    @Test
    void whenIncompletePython3Code_thenReturnLexedTokens() {
        String code = "print(";
        String expectedLexingResult = "{ startIndex=0, endIndex=4, tokenId=42 }, { startIndex=5, endIndex=5, tokenId=54 }";

        assertEquals(expectedLexingResult, annotationService.annotateCode(code, PYTHON));
    }

    @Test
    void whenJavaCodeCanNotBeLexed_thenFailGracefully() {
        String code = "\"{ emptyResult }";

        assertTrue(annotationService.annotateCode(code, JAVA).isEmpty());
    }
}