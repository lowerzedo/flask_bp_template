# Flask Blueprint Template

A production-ready Flask application template with a modular structure, designed to serve as a reference for building scalable REST APIs. This template includes authentication, database connections, and AWS Lambda deployment capabilities.

## 🌟 Features

- **Modular Architecture** using Flask Blueprints
- **Multiple Database Support**
  - MySQL
  - MSSQL
  - Oracle
- **Authentication Systems**
  - Microsoft Authentication
  - CAS (Central Authentication Service)
- **AWS Integration**
  - Lambda-ready configuration
  - CloudWatch logging support
- **Development Tools**
  - Docker support
  - Comprehensive testing setup
  - Code formatting (Black)
  - Linting (Flake8)

## 🏗️ Project Structure

```plaintext
app/
├── __init__.py          # Application factory
├── config.py            # Configuration settings
├── controllers/         # Request handlers
├── database/            # Database connection decorators
├── models/              # Database models and queries
├── routes/              # API route definitions
├── schemas/             # Request/Response validation schemas
├── services/            # Business logic
├── tests/               # Test suites
└── utils/               # Utility functions and decorators
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
  - If you don't have Oracle DB connections you may choose newer version of Python
- Docker (optional)
- MySQL/MSSQL/Oracle DB connection(s)

### Local Development Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd flask_bp_template
```

2. Install dependencies:

```bash
make setup
```

3. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:

```bash
make run
```

### Docker Setup

Docker is here to simulate the runtime environment of AWS Lambda for specific test cases. If you want to test in the local env, I'd recommend to create another docker file with Python slim image.

1. Build the Docker image:

```bash
make docker-build
```

2. Run the container:

```bash
make docker-run
```

## 📝 API Documentation

### User Management Endpoints

- POST /example/user
  - Creates a new user
  - Requires authentication
  - Validates request body using Pydantic schemas

## 🔒 Authentication

The template supports two authentication methods:

1. Microsoft Authentication

   - Token-based authentication
   - Group-based access control

2. CAS Authentication

   - Ticket-based authentication
   - Integration with existing CAS servers

## 🛠️ Development Tools

- Testing : make test
- Linting : make lint
- Code Formatting : make format
- Clean Build : make clean

## 🚀 Deployment

### CI/CD Pipeline

The project includes a Bitbucket-pipelines YAML file for automated testing, linting, and deployment.

### AWS Lambda Deployment

The template is configured for AWS Lambda deployment using Zappa:

```bash
zappa deploy dev    # Deploy to development
zappa deploy prod   # Deploy to production
```

Configuration is managed through zappa-settings.json .

## 🔍 Logging

- Development: Logs to both console and logs/app.log
- Production: Structured JSON logging for CloudWatch

## ✅ Validation Options

The template supports two validation approaches:

### Pydantic Validation

### Marshmallow Validation

Key differences:

- **Pydantic**: Type hints, runtime validation, better IDE support
- **Marshmallow**: More flexible serialization, legacy support, extensive validation options

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📄 License

This project is licensed under the MIT License.
