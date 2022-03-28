FROM node:16-alpine as development

WORKDIR /usr/src/app

# Copy package json and lock file to container image
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy local code to container image
COPY . .

# Expose API Port
EXPOSE 3000

# Run web service
CMD [ "npm", "start" ]