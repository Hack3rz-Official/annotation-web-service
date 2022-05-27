package com.hack3rz.annotationservice;

import com.hack3rz.annotationservice.repository.AnnotationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

/**
 * The main SpringBoot application to run the API
 */
@SpringBootApplication()
@EnableMongoRepositories
public class AnnotationServiceApplication {

    @Autowired
    AnnotationRepository annotationRepository;

    public static void main(String[] args) {
        SpringApplication.run(AnnotationServiceApplication.class, args);
    }

}
