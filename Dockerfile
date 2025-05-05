# Use official lightweight Node.js image
FROM node:14

# Create app directory
WORKDIR /app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY . .

# Expose port
EXPOSE 3000

# Command to run the app
CMD ["npm", "start"]

