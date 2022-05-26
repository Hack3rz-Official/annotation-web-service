package com.hack3rz.annotationservice;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

/**
 * Test configuration
 * Does not enable any async behaviour which facilitates testing
 */
@Configuration
@Profile("test")
public class TestConfiguration {
}
