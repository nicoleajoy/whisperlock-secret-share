# WhisperLock - Secure Secret Sharing Service

WhisperLock is a web application that allows users to securely share sensitive information through one-time-use URLs. Once a secret is viewed, it is permanently deleted from the database, ensuring that sensitive information cannot be accessed multiple times.

## Features

- One-time secret sharing through unique URLs
- End-to-end encryption using Fernet (symmetric encryption)
- Automatic deletion after viewing
- Docker containerization for easy deployment
- PostgreSQL database for secure storage

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Start the services using Docker Compose:
```bash
docker compose up -d
```

The application will be available at `http://localhost:5000`.

## Architecture

The project consists of two main services:

- **Web Service**: A Flask application that handles the web interface and secret management
- **Database Service**: A PostgreSQL database that stores encrypted secrets

### Security Features

- Secrets are encrypted before storage using Fernet symmetric encryption
- Each secret has its own unique encryption key
- Secrets are stored in binary format (BYTEA) in the database
- One-time access: secrets are deleted immediately after viewing
- No plaintext storage of sensitive information
- Unique randomly generated paths for secret URLs

## Environment Variables

The application supports the following environment variables:

- `DATABASE_URL`: PostgreSQL connection string (default: `postgresql://postgres:pgpassword@db:5432/postgres`)

## Development

The project uses Python 3.12 and requires the following main dependencies:
- Flask
- psycopg2
- cryptography
- python-dotenv

### Project Structure

```
.
├── docker-compose.yaml   # Docker Compose configuration
├── docker/
│   ├── db/               # Database initialization scripts
│   │   └── init.sql      # Initial schema and table creation
│   └── web/              # Web service files
│       ├── Dockerfile    # Web service container configuration
│       ├── app.py        # Main Flask application
│       ├── requirements.txt
│       ├── static/       # CSS files
│       └── templates/    # HTML files
└── README.md
```

### Database Schema

The application uses a dedicated schema `secrets_schema` with a `secrets_table` that has the following structure:

```sql
CREATE TABLE secrets_schema.secrets_table (
    id SERIAL PRIMARY KEY,
    fkey BYTEA UNIQUE NOT NULL,
    value BYTEA UNIQUE NOT NULL,
    path VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```

## Usage

1. Visit the homepage at `http://localhost:5000`
2. Enter the secret message you want to share
3. Submit the form to receive a unique URL
4. Share the URL with the intended recipient
5. The recipient can view the secret exactly once by visiting the URL

## Security Considerations

- Secrets are automatically deleted after viewing
- Each secret uses a unique encryption key
- All secrets are encrypted before storage
- URLs are randomly generated using cryptographically secure methods
- Database credentials should be changed in production

## Production Deployment

For production deployment, make sure to:

1. Change the database credentials
2. Use environment variables for sensitive configuration
3. Enable HTTPS
4. Configure appropriate security headers
5. Set up proper logging
6. Configure backup strategies
