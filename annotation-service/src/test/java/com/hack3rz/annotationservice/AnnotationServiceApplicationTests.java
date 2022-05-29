package com.hack3rz.annotationservice;

import com.hack3rz.annotationservice.controller.AnnotationController;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class AnnotationServiceApplicationTests {

    @Autowired
    private AnnotationController controller;

    /**
     * Tests that the application context is loaded and
     * that the autowired dependency injection works
     * @throws Exception exception thrown during application context building
     */
    @Test
    void contextLoads() throws Exception {
        assertThat(controller).isNotNull();
    }

}
