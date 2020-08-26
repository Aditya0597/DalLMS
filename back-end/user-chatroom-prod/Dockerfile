# Using the official nodejs image.
FROM node:14
# Work directory.
WORKDIR /app
# Copy the package manager file to the working location.
COPY package*.json ./
# Installing packages inside the image filesystem.
RUN npm install
# Copy source code to image filesystem.
COPY . .
# Docker image port.
EXPOSE 8080
# Command to run the application
CMD ["npm", "start"]