import http from 'k6/http';
import { sleep } from 'k6';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";


export const options = {
    stages: [
        { duration: '10s', target: 5 },
        //{ duration: '10s', target: 100 },
        //{ duration: '10s', target: 1000 },
        //{ duration: '1m30s', target: 10 },
        //{ duration: '20s', target: 0 },
    ],
};

export default function () {

    const url = 'http://localhost:3000/highlight';
    const payload = JSON.stringify({
        "code": "public static void main(String args[]){ System.out.println(\"testing\") }",
        "language": "java"
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    http.post(url, payload, params);
}

export function handleSummary(data) {
    return {
        "summary.html": htmlReport(data),
    };
}