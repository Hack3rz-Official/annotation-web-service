package com.hack3rz.annotationservice;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * The default configuration for the SpringBoot Application
 */
@Configuration
@EnableAsync
@Profile("!test")
public class ApplicationConfiguration {
}
