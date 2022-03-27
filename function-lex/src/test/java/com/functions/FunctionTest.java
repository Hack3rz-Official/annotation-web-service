/**
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for
 * license information.
 */
package com.functions;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.microsoft.azure.functions.*;
import org.apache.commons.text.StringEscapeUtils;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.stubbing.Answer;

import java.util.*;
import java.util.logging.Logger;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;


/**
 * Unit test for Function class.
 */
public class FunctionTest {

    /**
     * Unit test for Lex method with Java language.
     */
    @Test
    public void testLexJava() throws Exception {
        HttpResponseMessage ret = sendLexRequest(
            "java",
            "public static void main(String[] args) {}"
        );

        // Verify
        // TODO: currently we only verify that there are values in the body
        //  and that they can be deserialized to an integer list, not that the values are correct

        assertEquals(ret.getStatus(), HttpStatus.OK);
        assertNotNull(ret.getBody());
        assertNotEquals("", ret.getBody());

        ObjectMapper mapper = new ObjectMapper();
        List token_ids = mapper.readValue(ret.getBody().toString(), List.class);
        assertNotEquals(0, token_ids.size());
    }

    /**
     * Unit test for Lex method with Java language.
     */
    @Test
    public void testLexKotlin() throws Exception {
        HttpResponseMessage ret = sendLexRequest(
            "kotlin",
            "fun main() { println(\"Hello, World!\") }"
        );

        // Verify
        // TODO: currently we only verify that there are values in the body
        //  and that they can be deserialized to an integer list, not that the values are correct

        assertEquals(ret.getStatus(), HttpStatus.OK);
        assertNotNull(ret.getBody());
        assertNotEquals("", ret.getBody());

        ObjectMapper mapper = new ObjectMapper();
        List token_ids = mapper.readValue(ret.getBody().toString(), List.class);
        assertNotEquals(0, token_ids.size());
    }

    /**
     * Unit test for Lex method with Java language.
     */
    @Test
    public void testLexPython() throws Exception {
        HttpResponseMessage ret = sendLexRequest(
            "python",
            "print(\"Hello World\")"
        );

        // Verify
        // TODO: currently we only verify that there are values in the body
        //  and that they can be deserialized to an integer list, not that the values are correct

        assertEquals(ret.getStatus(), HttpStatus.OK);
        assertNotNull(ret.getBody());
        assertNotEquals("", ret.getBody());

        ObjectMapper mapper = new ObjectMapper();
        List token_ids = mapper.readValue(ret.getBody().toString(), List.class);
        assertNotEquals(0, token_ids.size());
    }

    /**
     * Unit test for Lex method with incomplete Java language.
     */
    @Test
    public void testLexIncompleteJava() throws Exception {
        HttpResponseMessage ret = sendLexRequest(
            "java",
            "public static void mai}"
        );

        // Verify
        // TODO: currently we only verify that there are values in the body
        //  and that they can be deserialized to an integer list, not that the values are correct

        assertEquals(ret.getStatus(), HttpStatus.OK);
        assertNotNull(ret.getBody());
        assertNotEquals("", ret.getBody());

        ObjectMapper mapper = new ObjectMapper();
        List token_ids = mapper.readValue(ret.getBody().toString(), List.class);
        assertNotEquals(0, token_ids.size());
    }

    /**
     * Sends a request to the lexing function
     * @param language the language for the request
     * @param code the source code
     * @return the http response of the function
     */
    private HttpResponseMessage sendLexRequest(String language, String code) {
        // Setup
        @SuppressWarnings("unchecked")
        final HttpRequestMessage<Optional<String>> req = mock(HttpRequestMessage.class);

        final Map<String, String> queryParams = new HashMap<>();
        doReturn(queryParams).when(req).getQueryParameters();

        code = StringEscapeUtils.escapeJson(code);

        String body = "{ \"lang_name\": \"" + language + "\", \"code\": \"" + code + "\" }";

        final Optional<String> queryBody = Optional.of(body);
        doReturn(queryBody).when(req).getBody();

        doAnswer(new Answer<HttpResponseMessage.Builder>() {
            @Override
            public HttpResponseMessage.Builder answer(InvocationOnMock invocation) {
                HttpStatus status = (HttpStatus) invocation.getArguments()[0];
                return new HttpResponseMessageMock.HttpResponseMessageBuilderMock().status(status);
            }
        }).when(req).createResponseBuilder(any(HttpStatus.class));

        final ExecutionContext context = mock(ExecutionContext.class);
        doReturn(Logger.getGlobal()).when(context).getLogger();

        // Invoke
        final HttpResponseMessage ret = new Function().lex(req, context);

        return ret;
    }

}
