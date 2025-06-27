# Use Node.js official image
FROM node:latest

# Set working directory
WORKDIR /usr/src/app

# Install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get clean  && npm install && rm -rf /var/lib/apt/lists/*

# Expose the application port
EXPOSE 8801

VOLUME [ "/usr/src/app/public", "/usr/src/app/pages" ]
# Copy the application files
COPY ./config/node_cv/public /usr/src/app/public
COPY ./config/node_cv/pages /usr/src/app/pages
COPY ./config/node_cv/my-cv.js /usr/src/app/my-cv.js
# Copy the package.json file
COPY ./config/node_cv/package.json /usr/src/app/package.json
# Install application dependencies
RUN npm install
# Set environment variables
ENV PORT=8801
ENV NODE_ENV=production

# Start the Node.js app and keep it running
CMD ["node", "my-cv.js"]
