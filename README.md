# Recommendation System

This project implements a simple recommendation system composed of multiple services, each encapsulated within Docker containers. The system includes a **Generator Service** that creates recommendations and an **Invoker Service** that manages and retrieves these recommendations.

## Overview

The recommendation system consists of two primary services:

- **Generator Service**: Generates random recommendations based on a specified model name and viewer ID.
- **Invoker Service**: Retrieves recommendations from a cache or calls the Generator Service when the data is not cached.

## Services

### Generator Service

- **Endpoint**: `POST /generate`
- **Description**: This endpoint generates a random recommendation based on the provided model name and viewer ID.
- **Request Body**:
  ```json
  {
    "modelname": "ModelA",
    "viewerid": "123"
  }
  ```

- **Response Example**:
  ```json
  {
    "reason": "ModelA",
    "result": 42
  }
  ```

### Invoker Service

- **Endpoint**: `POST /recommend`
- **Description**: This endpoint retrieves recommendations for a specified viewer ID. If the data is not available in the cache, it triggers the Generator Service to fetch new recommendations.
- **Request Body**:
  ```json
  {
    "viewerid": "123"
  }
  ```

- **Response Example**:
  ```json
  {
    "ModelA": 39,
    "ModelB": 94,
    "ModelC": 74,
    "ModelD": 100,
    "ModelE": 89
  }
  ```

## Setup and Running the Project

1. **Clone the Repository**: 
   ```bash
   git clone <repository-url>
   cd recommendation-system
   ```

2. **Build the Docker Containers**: 
   ```bash
   docker-compose build
   ```

3. **Start the Services**:
   ```bash
   docker-compose up
   ```

## Testing the Services

You can test the services using a tool like Postman or curl.

- **Generator Service**:
  - **URL**: `http://localhost:5000/generate`
  - **Example Request**:
    ```bash
    curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"modelname": "ModelA", "viewerid": "123"}'
    ```

- **Invoker Service**:
  - **URL**: `http://localhost:5001/recommend`
  - **Example Request**:
    ```bash
    curl -X POST http://localhost:5001/recommend -H "Content-Type: application/json" -d '{"viewerid": "123"}'
    ```

## Conclusion

This recommendation system demonstrates the use of microservices architecture, Docker, and caching strategies to efficiently generate and retrieve recommendations.
```
