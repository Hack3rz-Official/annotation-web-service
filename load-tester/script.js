import http from 'k6/http';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";


/**
 * The stages will be run in sequence.
 * Target specifies the number of concurrent users.
 * Duration specifies the duration of the stage.
 */
export const options = {
    stages: [
        { duration: '10s', target: 1 },
        { duration: '10s', target: 5 },
        //{ duration: '10s', target: 100 },
        //{ duration: '10s', target: 1000 },
        //{ duration: '1m30s', target: 10 },
        //{ duration: '20s', target: 0 },
    ],
};

/**
 * The test file that will be sent to the API.
 */
const testFile = open("samples/java/FunctionTest.java");

export default function () {

    const url = 'http://localhost:8081/api/v1/highlight';
    const payload = JSON.stringify({
        "code": testFile,
        "language": "java"
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    http.post(url, payload, params);
}

/**
 * This will produce a summary.html output file
 */
export function handleSummary(data) {
    return {
        "summary.html": htmlReport(data),
    };
}