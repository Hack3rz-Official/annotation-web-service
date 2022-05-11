import axios from "axios";
import { useSettingsStore } from "../stores/settingsStore";

// default axios instance
export const axiosDefault = axios.create({});

// create request limited axios instance
export const axiosLimited = axios.create({});

/*
* This timeout wrapper is a workaround to use pinia store outside of components.
* https://pinia.vuejs.org/core-concepts/outside-component-usage.html#single-page-applications
*/
setTimeout(() => {
  const settingsStore = useSettingsStore();

  // Axios Request Interceptor
  axiosLimited.interceptors.request.use(function (config) {
    return new Promise((resolve, reject) => {
      let interval = setInterval(() => {
        if (settingsStore.pendingRequests < settingsStore.maxRequests) {
          settingsStore.pendingRequests++;
          console.log(`Request sent - Pending requests: ${settingsStore.pendingRequests}`);
          config.meta = config.meta || {};
          config.meta.requestStartedAt = new Date().getTime();
          console.log({ config });
          clearInterval(interval);
          resolve(config);
        }
      }, settingsStore.interval);
    });
  });

  // Axios Response Interceptor
  axiosLimited.interceptors.response.use(
    function (response) {
      settingsStore.pendingRequests = Math.max(0, settingsStore.pendingRequests - 1);
      response.responseTime = new Date().getTime() - response.config.meta.requestStartedAt;
      console.log(`Request resolved - Pending requests: ${settingsStore.pendingRequests}`);
      console.log({ response });
      return Promise.resolve(response);
    },
    function (error) {
      settingsStore.pendingRequests = Math.max(0, settingsStore.pendingRequests - 1);
      response.responseTime = new Date().getTime() - response.config.meta.requestStartedAt;
      console.log(`Request resolved - Pending requests: ${settingsStore.pendingRequests}`);
      return Promise.reject(error);
    }
  );
}, 1);
