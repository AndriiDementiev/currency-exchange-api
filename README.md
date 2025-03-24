# CurrencyExchange API

**CurrencyExchange API** is a Django-based application that provides currency exchange rates, user balance management, and transaction history. The API integrates with an external ExchangeRate API, uses JWT authentication, and is fully containerized using Docker and managed via Poetry.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation & Configuration](#installation--configuration)
- [Running the Project with Docker Compose](#running-the-project-with-docker-compose)
- [Database Migrations](#database-migrations)
- [API Endpoints](#api-endpoints)
- [Admin Panel](#admin-panel)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)

---

## Features

- **User Registration:** Create a new user account with an initial balance of 1000 coins.
- **User Balance:** Retrieve the current coin balance of the authenticated user.
- **Currency Exchange:** Get exchange rates for a given currency, deduct a coin from the balance, and log the transaction.
- **Exchange History:** View previous exchange transactions with optional filtering by currency code and date.
- **JWT Authentication:** Secure API endpoints using JWT tokens.
- **Interactive API Documentation:** Swagger and Redoc documentation.
- **Admin Panel:** Enhanced Django Admin for managing users and transactions.
- **Fully Dockerized:** The project runs via Docker Compose with PostgreSQL.

---

## Requirements

- Python 3.12
- PostgreSQL
- Docker & Docker Compose
- Poetry

---

## Installation & Configuration

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AndriiDementiev/currencyexchange-api.git
   cd currencyexchange-api
   ```

2. **Configure Environment Variables:**

   Copy the provided `.env.sample` file to `.env`:

   ```bash
   cp .env.sample .env
   ```

   Edit the `.env` file and update the values:

   ```ini
   SECRET_KEY=your-secret-key

   # PostgreSQL settings
   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432

   # ExchangeRate API
   EXCHANGE_RATE_API_KEY=your-exchange-rate-api-key
   EXCHANGE_RATE_API_URL=https://v6.exchangerate-api.com/v6
   ```

   **Note:** These variables are automatically injected into the container via Docker Compose.

---

## Running the Project with Docker Compose

To build and run the application and database, use:

```bash
docker-compose up --build
```

The project will be available at: [http://localhost:8001](http://localhost:8001)

---

## Database Migrations

After the containers are running, apply migrations:

```bash
docker-compose exec web poetry run python manage.py migrate
```

Create a superuser if needed:

```bash
docker-compose exec web poetry run python manage.py createsuperuser
```

---

## API Endpoints

### POST `/api/register/`
**Register a new user.**

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Responses:**
- `201 Created`: User registered successfully.
- `400 Bad Request`: Validation error.

### GET `/api/balance/`
**Retrieve user balance.**

**Responses:**
- `200 OK`: Returns the balance.
- `404 Not Found`: Balance not found.

### POST `/api/currency/`
**Get currency exchange rate.**

**Request Body:**

```json
{
  "currency_code": "string"
}
```

**Responses:**
- `200 OK`: Success, returns exchange rate and updated balance.
- `400 Bad Request`: Invalid currency code.
- `403 Forbidden`: Insufficient balance.
- `500 Server Error`: Exchange rate API error.

### GET `/api/history/`
**Retrieve exchange history.**

**Query Parameters:**
- `currency_code` (string): Filter by currency.
- `date` (YYYY-MM-DD format): Filter by date.

**Responses:**
- `200 OK`: Returns a list of exchange records.

---

## Admin Panel

The project includes a **Django Admin Panel**.

### **Access the admin panel**:

- URL: [http://localhost:8001/admin/](http://localhost:8001/admin/)
- Log in with the superuser credentials.
- Manage users, transactions, and balances.

---

## API Documentation

Available at:

- **Swagger UI:** [http://localhost:8001/swagger/](http://localhost:8001/swagger/)
- **Redoc UI:** [http://localhost:8001/redoc/](http://localhost:8001/redoc/)

---

## Running Tests

Run the tests:

```bash
docker-compose exec web poetry run python manage.py test currency_exchange.tests
