# Use an official Python runtime as the base image
FROM python:3.9.16-alpine

# Set the working directory
WORKDIR /app

# Copy the current directory to the working directory
COPY . .

# Install the required packages
RUN apk update && \
    apk add mysql-client && \
    apk add mysql-dev && \
    apk add build-base && \
    apk add libxml2-dev libxslt-dev && \
    apk add python3-dev && \
    pip install mysql-connector-python && \
    pip install beautifulsoup4 && \
    pip install requests

# Set the environment variables to be passed at runtime
ENV HOST ""
ENV PORT ""
ENV USERNAME ""
ENV PASSWORD ""
ENV DB_NAME ""

# Run the command to start the program
CMD ["python", "main.py"]
