package com.hack3rz.annotationservice.repository;

import com.hack3rz.annotationservice.model.Annotation;
import com.hack3rz.annotationservice.model.Annotation.AnnotationKey;
import org.jetbrains.annotations.NotNull;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository that handles the interaction with the mongo database for the annotation models.
 */
@Repository
public interface AnnotationRepository extends MongoRepository<Annotation, String> {

    Annotation findAnnotationById(AnnotationKey id);

    Boolean existsAnnotationBySourceCode(String code);

    @NotNull
    List<Annotation> findAll();

    public long count();
}
