export default () => ({
  service: {
    port: process.env.WEB_API_PORT,
  },
  lex: {
    url: process.env.LEX_URL,
  },
  predict: {
    url: process.env.PREDICT_URL,
  },
});