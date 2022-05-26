package com.hack3rz.annotationservice.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

import java.util.ArrayList;
import java.util.List;

/**
 * Custom Exception for the REST endpoint
 */
@Getter
public class ApiException  extends RuntimeException {

    private final HttpStatus status;
    private final String message;
    private final List<String> errors;

    public ApiException(HttpStatus status, String message) {
        super();
        this.status = status;
        this.message = message;
        this.errors = new ArrayList<>();
    }

    public ApiException(HttpStatus status, String message, String error) {
        super();
        this.status = status;
        this.message = message;
        this.errors = List.of(error);
    }

    public ApiException(HttpStatus status, String message, List<String> errors) {
        super();
        this.status = status;
        this.message = message;
        this.errors = errors;
    }
}
