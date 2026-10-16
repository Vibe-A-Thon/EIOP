FROM node:22.20.0-alpine
WORKDIR /extension
COPY package.json package-lock.json ./
RUN npm ci
COPY extension.js README.md .vscodeignore ./
CMD ["npm", "run", "package"]
