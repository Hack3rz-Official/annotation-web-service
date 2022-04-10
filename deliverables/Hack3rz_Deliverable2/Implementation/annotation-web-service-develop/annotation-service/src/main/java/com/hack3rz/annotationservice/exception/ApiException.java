package com.hack3rz.annotationservice.exception;

import java.util.List;

import org.springframework.http.HttpStatus;

import lombok.Getter;

@Getter
public class ApiException  extends RuntimeException {

    private HttpStatus status;
    private String message;
    private List<String> errors;

    public ApiException(HttpStatus status, String message) {
        super();
        this.status = status;
        this.message = message;
    }

    public ApiException(HttpStatus status, String message, String error) {
        super();
        this.status = status;
        this.message = message;
        errors = List.of(error);
    }

    public ApiException(HttpStatus status, String message, List<String> errors) {
        super();
        this.status = status;
        this.message = message;
        this.errors = errors;
    }
}
