# MyPet Project - README

## Project Overview

**MyPet** is a comprehensive platform designed to enhance the experience of pet owners by providing services related to pet care, lost and found pets, and local pet service providers. The application centralizes essential pet-related services and notifications within a unified interface.

### Key Features

1. **Pet Profile Management**:
   - Manage pet profiles with details such as medical history, vaccinations, and images.
   - Keep all pet-related information secure and accessible.

2. **Lost Pet Reports and Matching**:
   - Submit lost pet reports and search for found pets.
   - Receive real-time notifications when matching pets are found using a matching algorithm.

3. **Local Pet Services Finder**:
   - Discover local pet services like veterinarians, pet sitters, and trainers.
   - Integrated GIS and GPS for accurate location-based services.

4. **Notification System**:
   - Real-time alerts for lost pet matches, updates on pet services, and reminders for pet care activities.
   - WebSocket-based notifications for instant communication.

### Problem Addressed

MyPet aims to solve the common issues pet owners face, such as keeping track of health records, finding lost pets, and accessing local services. By bringing these functions together into one app, MyPet simplifies pet care management.

## API Endpoints

### Users
- **Register a User**: `POST /users/`
- **Login**: `POST /users/login/`
- **List Users**: `GET /users/`
- **Get User by ID**: `GET /users/{user_id}/`
- **Verify Email**: `GET /users/verify-email/{user_id}/{token}/`
- **Reset Token**: `POST /users/reset-token/`
- **Update User Details**: `PUT /users/update-details/{user_id}`

### Pets
- **Manage Pet Profiles**: `GET, POST, PUT /pets/`

### Lost Pet Reports
- **Create Lost Pet Report**: `POST /lost_pet_reports/`
- **List Lost Pet Reports**: `GET /lost_pet_reports/`

### Found Pet Reports
- **Create Found Pet Report**: `POST /found_pet_reports/`
- **List Found Pet Reports**: `GET /found_pet_reports/`

### Avatar Images
- **Upload and Manage Avatar Images**: `POST, GET /avatar_images/`

### Medical History
- **Manage Medical History Records**: `GET, POST, PUT /medical_history/`

### Service Providers
- **Find and Manage Pet Service Providers**: `GET, POST, PUT /service_providers/`

### Working Hours
- **Manage Service Provider Working Hours**: `GET, POST, PUT /working_hours/`

### Provider Phones
- **Manage Service Provider Contact Information**: `GET, POST /provider_phones/`

### User-Provider Associations
- **Manage Associations between Users and Providers**: `GET, POST, DELETE /users_providers/`

### Service Provider Locations
- **Manage Locations for Service Providers**: `GET, POST, PUT /service_provider_locations/`

## Architecture and Technology Stack

- **Backend**: FastAPI, PostgreSQL with PostGIS for spatial data management.
- **Mobile App**: Android development for end-user interaction.
- **Mapping & GIS Integration**: Integrated with PostGIS for managing geographic data.
- **Authentication**: OAuth2 with JWT-based authentication and role-based access control.
- **Notifications**: Real-time notifications using WebSocket for push updates.
- **Containerization**: Docker Compose for service orchestration (database setup using PostGIS and PgAdmin).

## Getting Started

### Prerequisites

- **Python 3.8+**
- **FastAPI**
- **PostgreSQL with PostGIS**
- **Docker & Docker Compose**
- **Android Development Environment**

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/username/mypet.git
   ```

2. Set up environment variables in a `.env` file:

   ```bash
   JWT_SECRET_KEY=your_secret_key
   ACCESS_TOKEN_EXPIRE_MINUTES=240
   DATABASE_URL=postgresql://user:password@localhost/mypetdb
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database using Docker:

   ```bash
   docker-compose up -d
   ```

5. Apply migrations to create the database schema:

   ```bash
   alembic upgrade head
   ```

6. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

### Running the Application

After setting up the environment, use the following command to run the API server:

```bash
uvicorn app.main:app --reload
```

Access the API via Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs).

## Docker Compose Setup

To set up the database services, run the following command:

```bash
docker-compose up -d
```

This will start the PostgreSQL database and PgAdmin for managing the database via a graphical interface.

## License and Copyright

**MyPet** is developed by **Aviad Korakin**. All rights reserved.

This project is intended for educational purposes. Unauthorized distribution or commercial use is prohibited.
