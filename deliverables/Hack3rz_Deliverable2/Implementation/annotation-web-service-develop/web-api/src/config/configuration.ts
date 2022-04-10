export default () => ({
  service: {
    port: process.env.SERVICE_PORT
  },
  lex: {
    url: process.env.LEX_URL
  },
  predict: {
    url: process.env.PREDICT_URL
  }
});