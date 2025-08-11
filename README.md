# fast_api_boilerplate_alembic_sqlalchemy
This is the fast api boilerplate for starting a project.


# CivicQ


## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: OAuth2 with JWT
- **Storage**: S3 (for future implementation)

## Installation

### Prerequisites

- Python 3.13+
- PostgreSQL installed and running
- Virtual environment setup

### Setup Instructions

```sh
# Clone the repository

# Create and activate a virtual environment
python3.13 -m venv venv
source venv/bin/activate  # On Windows use `.env\Scripts\activate`

```


### Installing requirements

```sh
cd backend
# Install dependencies
pip install -r requirements.txt
```

### Database Configuration

Update the `.env` file with your database credentials:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/db_name
```

Apply Already Created Migrations (Upgrade):

```sh
alembic upgrade head
```

Create new Migration:

```sh
alembic revision --autogenerate -m ""
```

Revert latest one Migration (Downgrade):

```sh
alembic downgrade -1
```

You can also downgrade to a specific revision::

```sh
alembic downgrade <revision_id>
```

To see revision history:

```sh
alembic history
```

## Freeze package to requirements.txt guide

(1) write package name in requirements.in manually:

```sh
pip-compile requirements.in
```

(2) write package name in requirements.in manually:

```sh
pip install -r requirements.txt
```

## Running the Application

```sh
uvicorn app.main:app --reload
```

## Visit Admin Dashboard

http://127.0.0.1:8000/admin

## Introduction

CivicQ is a civic engagement platform designed to bring transparency and accountability to U.S. politics. The website will serve as a centralized hub for users to explore representatives’ profiles, track legislative activity, view social and fiscal scores of legislation and officials, and participate in public discourse through news aggregation, voting insights, and community feedback features.

## Features

- User authentication and role management (Admin, User)



## Future Enhancements

## License

This project is licensed under the MIT License.

---



