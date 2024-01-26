# Volvo Flask Application Deployment Guide

Welcome to the Volvo Flask Application deployment guide. This document provides instructions for setting up and deploying the Flask application hosted within this repository to AWS Elastic Beanstalk using Docker.

## Application Overview

The Volvo Flask Application is a simple web service written in Python using the Flask framework. It's designed to run within a Docker container and is easy to deploy on AWS Elastic Beanstalk.

## Repository Structure

- `app.py`: The Flask application entry point.
- `Dockerfile`: Instructions for Docker to build the application image.
- `requirements.txt`: Python dependencies required by the application.
- `Dockerrun.aws.json`: Configuration for AWS Elastic Beanstalk for running the Docker container.

## Prerequisites

Before you begin, ensure you have the following:

- An AWS account with access to Elastic Beanstalk, IAM, and ECR services.
- AWS CLI installed and configured with the necessary access rights.
- Docker installed on your local machine for testing and image creation.

## Local Setup and Testing

1. **Clone the Repository:**

   Clone the repository to your local machine and navigate to the directory.

   ```sh
   git clone https://github.com/your-username/volvo-flask-app.git
   cd volvo-flask-app
   ```
## Build the Docker image

To build the Docker image, run the following command in your terminal:

```bash
docker build -t volvo-flask-app:latest .
```

## Running the Application

After the image has been successfully built, you can run the application with Docker using the following command:

```bash
docker run -p 80:80 volvo-flask-app:latest
```
The application will then be accessible at http://localhost.
Make sure you execute these commands in the root directory of your project, where the Dockerfile is located.

## Deployment

This application is configured for deployment to AWS Elastic Beanstalk using the `Dockerrun.aws.json` provided. You can deploy the application using the AWS Management Console or the AWS CLI.

Refer to [AWS documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker.html) for details on deploying Docker containers.

## Configuration

The `Dockerrun.aws.json` file is configured to pull the image from the public ECR repository and expose it on port 80:

```json
{
  "AWSEBDockerrunVersion": "1",
  "Image": {
    "Name": "public.ecr.aws/z5w2y1r2/volvo:latest",
    "Update": "true"
  },
  "Ports": [
    {
      "ContainerPort": "80"
    }
  ]
}

## Contributing

We welcome suggestions for improving the app! If you'd like to contribute:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Don't forget to give the project a star! Your contributions are greatly appreciated.

