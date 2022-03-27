/**
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for
 * license information.
 */

package com.functions;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.microsoft.azure.functions.ExecutionContext;
import com.microsoft.azure.functions.HttpMethod;
import com.microsoft.azure.functions.HttpRequestMessage;
import com.microsoft.azure.functions.HttpResponseMessage;
import com.microsoft.azure.functions.HttpStatus;
import com.microsoft.azure.functions.annotation.AuthorizationLevel;
import com.microsoft.azure.functions.annotation.FixedDelayRetry;
import com.microsoft.azure.functions.annotation.FunctionName;
import com.microsoft.azure.functions.annotation.HttpTrigger;

import java.util.Optional;

import resolver.JavaResolver;


import java.util.Arrays;

import lexer.LTok;

/**
 * Azure Functions with HTTP Trigger.
 */
public class Function {

    /**
     * This function listens at endpoint "/api/lex". Two ways to invoke it using "curl" command in bash:
     * curl -d "HTTP Body" {your host}/api/lex
     */
    @FunctionName("Lex")
    public HttpResponseMessage lex(
        @HttpTrigger(
            name = "req",
            methods = {HttpMethod.GET, HttpMethod.POST},
            authLevel = AuthorizationLevel.ANONYMOUS)
            HttpRequestMessage<Optional<String>> request,
        final ExecutionContext context) {

        context.getLogger().info("Java HTTP trigger processed a request.");


        // Parse query parameter
        final String query = request.getQueryParameters().get("code");
        final String code = request.getBody().orElse(query);

        if (code == null) {
            return request.createResponseBuilder(HttpStatus.BAD_REQUEST).body("Please pass code on the query string or in the request body").build();
        } else {

            JavaResolver resolver = new JavaResolver();
            LTok[] lToks = resolver.lex(code);

            if (lToks != null) {
                Integer[] ids = Arrays.stream(lToks).map(tok -> tok.tokenId).toArray(size -> new Integer[lToks.length]);
                String json = null;
                try {
                    json = new ObjectMapper().writeValueAsString(ids);
                } catch (JsonProcessingException e) {
                    return request.createResponseBuilder(HttpStatus.INTERNAL_SERVER_ERROR).body("Could not convert token array to JSON: " + e.getMessage()).build();
                }
                return request.createResponseBuilder(HttpStatus.OK).body(json).build();
            } else {
                return request.createResponseBuilder(HttpStatus.BAD_REQUEST).body("Code could not be lexed.").build();
            }


        }
    }

}
