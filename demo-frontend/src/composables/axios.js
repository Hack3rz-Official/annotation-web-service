import axios from "axios";

const MAX_REQUESTS_COUNT = 1;
const INTERVAL_MS = 10;
let PENDING_REQUESTS = 0;

// default axios instance
export const axiosDefault = axios.create({});

// create request limited axios instance 
export const axiosLimited = axios.create({});

// Axios Request Interceptor
axiosLimited.interceptors.request.use(function (config) {
  return new Promise((resolve, reject) => {
    let interval = setInterval(() => {
      if (PENDING_REQUESTS < MAX_REQUESTS_COUNT) {
        PENDING_REQUESTS++;
        console.log(`Request sent - Pending requests: ${PENDING_REQUESTS}`);
        config.meta = config.meta || {};
        config.meta.requestStartedAt = new Date().getTime();
        console.log({ config });
        clearInterval(interval);
        resolve(config);
      }
    }, INTERVAL_MS);
  });
});

// Axios Response Interceptor
axiosLimited.interceptors.response.use(
  function (response) {
    PENDING_REQUESTS = Math.max(0, PENDING_REQUESTS - 1);
    console.log(`Request resolved - Pending requests: ${PENDING_REQUESTS}`);
    console.log({ response });
    return Promise.resolve(response);
  },
  function (error) {
    PENDING_REQUESTS = Math.max(0, PENDING_REQUESTS - 1);
    console.log(`Request resolved - Pending requests: ${PENDING_REQUESTS}`);
    return Promise.reject(error);
  }
);

axiosLimited.interceptors.response.use(
  (x) => {
    x.responseTime = new Date().getTime() - x.config.meta.requestStartedAt;
    return x;
  },
  // Handle 4xx & 5xx responses
  (x) => {
    x.responseTime = new Date().getTime() - x.config.meta.requestStartedAt;
    return x;
  }
);
