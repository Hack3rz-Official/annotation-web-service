package com.hack3rz.annotationservice.repository;

import com.hack3rz.annotationservice.model.Annotation;
import org.jetbrains.annotations.NotNull;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface AnnotationRepository extends MongoRepository<Annotation, String> {

    Annotation findAnnotationById(String id);

    @NotNull
    List<Annotation> findAll();

    public long count();
}
