package com.hack3rz.annotationservice.controller;

import com.hack3rz.annotationservice.enumeration.SupportedLanguage;
import com.hack3rz.annotationservice.service.AnnotationService;
import lexer.LTok;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.AutoConfigureDataMongo;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.notNullValue;
import static org.hamcrest.collection.IsCollectionWithSize.hasSize;
import static org.mockito.Mockito.doNothing;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AnnotationController.class)
@ComponentScan("com.hack3rz.annotationservice")
@ExtendWith(SpringExtension.class)
@ActiveProfiles(profiles = "test")
@AutoConfigureDataMongo
public class AnnotationControllerTest {

    @Autowired
    private MockMvc mvc;

    @MockBean
    private AnnotationService service;

    @Test
    public void whenPostAnnotateCode_thenReturnLexingTokens() throws Exception {
        SupportedLanguage language = SupportedLanguage.JAVA;
        String code = "public static void main(String[] args) {}";
        LTok[] lToks = {new LTok(0,1,1), new LTok(1,2,2)};

        // we mock the behaviour of the annotationService to not depend on it
        doNothing().when(service).persistCode(code, language);
        Mockito.when(service.lexCode(code, language)).thenReturn(lToks);


        String requestBody = "{ \"code\" : \"public static void main(String[] args) {}\", \"language\" : \"JAVA\"}";

        mvc.perform(post("/api/v1/annotation")
                .contentType(MediaType.APPLICATION_JSON).content(requestBody))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(2)))
                .andExpect(jsonPath("$[0].startIndex", notNullValue()))
                .andExpect(jsonPath("$[0].endIndex", notNullValue()))
                .andExpect(jsonPath("$[0].tokenId", notNullValue()));

    }
}
