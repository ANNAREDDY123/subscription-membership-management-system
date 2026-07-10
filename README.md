# subscription-membership-management-system
FastAPI Subscription &amp; Membership Management System with JWT Authentication, Membership Management, Subscription Management, Payment History, Reports, Search, SQLAlchemy ORM, Pagination, Logging, Docker Support, and Unit Tests.
# Subscription & Membership Management System

## Features

- JWT Authentication
- Membership Management (CRUD)
- Subscription Management
- Payment History
- Reports & Search
- SQLAlchemy ORM
- SQLite Database
- Docker Support
- Logging
- Basic Unit Tests



## Setup Instructions

### Install Dependencies


pip install -r requirements.txt


### Run Project


py -m uvicorn main:app --reload


Swagger


http://127.0.0.1:8000/docs


## Environment Variables


SECRET_KEY=subscription_secret_key
ALGORITHM=HS256


## API Examples

- POST `/auth/register`
- POST `/auth/login`
- POST `/members`
- POST `/subscriptions`
- POST `/payments`



## Docker Deployment


docker build -t subscription-system .
docker run -p 8000:8000 subscription-system


## Assumptions

- Only one active subscription per member.
- End date must be greater than the start date.
- Expired subscriptions cannot be modified.
- Payment amount must be greater than 0.
