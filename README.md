# Event Management System

## Overview
The Event Management System is a microservices-based application designed to manage event creation and notifications. This application is built using Flask for the microservices, PostgreSQL for the database, and Kubernetes for deployment, with each microservice independently scalable.

## Architecture Diagram
![Architecture Diagram](https://github.com/sathish-kumaresan/event-management-system/blob/master/Architecture_Diagram%20-%20Event_Management_System.jpg)

## Project Structure
- **event_service**: Handles event creation, retrieval, updating, and deletion (CRUD operations).
- **notification_service**: Sends notifications when a new event is created.
- **k8s-config**: Contains Kubernetes configuration files for deploying the services and the PostgreSQL database with persistent storage.

## Features
1. **REST API**: Both `event_service` and `notification_service` expose RESTful APIs.
2. **Persistent Storage**: The PostgreSQL database stores event information with persistent storage enabled for durability.
3. **Scalability**: Both microservices are independently scalable in Kubernetes.
4. **Notifications**: Sends notifications when new events are created, demonstrating inter-microservice communication.

## Deployment
The application is designed to be deployable on Kubernetes with Docker images hosted on Docker Hub.

### Prerequisites
- Docker
- Kubernetes
- PostgreSQL
- Git
- Postman (optional for testing)

### Step-by-Step Deployment
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/sathish-kumaresan/event-management-system.git
    cd event-management-system
    ```

2. **Docker Image Build and Push**:
   Ensure Docker images for `event_service` and `notification_service` are built and pushed to Docker Hub:
    ```bash
    docker build -t sathish6/event-service ./event_service
    docker build -t sathish6/notification-service ./notification_service
    docker push sathish6/event-service
    docker push sathish6/notification-service
    ```

3. **Kubernetes Deployment**:
   Deploy each service using Kubernetes configuration files located in the `k8s-config` directory:
    ```bash
    kubectl apply -f k8s-config/postgres-deployment.yaml
    kubectl apply -f k8s-config/event-deployment.yaml
    kubectl apply -f k8s-config/notification-deployment.yaml
    ```

4. **Port Forwarding for Testing**:
    ```bash
    kubectl port-forward service/event-service 5000:5000
    kubectl port-forward service/notification-service 5001:5001
    kubectl port-forward service/postgres 5432:5432
    ```

## Testing
### Using Postman
Import the `sample_postman_collection.json` in Postman to test the following endpoints:
1. **Create Event**: `POST /events`
2. **Retrieve Events**: `GET /events`
3. **Update Event**: `PUT /events/{id}`
4. **Delete Event**: `DELETE /events/{id}`

### Sample API Requests
- **Create Event**:
    ```json
    POST /events
    {
      "title": "Weekly Meeting",
      "description": "Project discussion",
      "date": "2024-11-15"
    }
    ```
- **Retrieve Events**:
    ```json
    GET /events
    ```

## Challenges and Future Improvements
- **Database Connection Issues**: Ensured connection stability between services in Kubernetes.
- **Scalability**: Enhanced by using Kubernetes replicas for the microservices.
- **Security**: Future improvements could include adding API tokens and encrypted storage for sensitive data.

## Repository
[Event Management System on GitHub](https://github.com/sathish-kumaresan/event-management-system)

