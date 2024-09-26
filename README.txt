# Django Transaction API Project

Welcome to the Django Transaction API Project! This is a RESTful API built using Django and Django REST Framework, designed to manage user accounts, wallets, and transactions. The project supports JWT authentication for secure access.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Windows](#installation-on-windows)
  - [macOS](#installation-on-macos)
  - [Linux](#installation-on-linux)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features

- User account management
- Wallet management
- Transaction handling
- JWT authentication
- RESTful API structure

## Prerequisites

- Python 3.8 or later
- pip (Python package installer)
- A virtual environment (recommended)

## Installation

### Installation on Windows

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/transaction_project.git
   cd transaction_project
   
2. Create a virtual environment:

bash
Copy code
python -m venv venv
venv\Scripts\activate


3. Install required packages:

bash
Copy code
pip install -r requirements.txt


### Installation on macOS
1. **Clone the repository:**

bash
Copy code
git clone https://github.com/yourusername/transaction_project.git
cd transaction_project

2. Create a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate

3. Install required packages:

bash
Copy code
pip install -r requirements.txt


### Installation on Linux
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/transaction_project.git
cd transaction_project
Create a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install required packages:

bash
Copy code
pip install -r requirements.txt


### Configuration
1.Create a .env file in the root of the project and add your secret keys:

Copy code
SECRET_KEY=your_secret_key
EXCHANGE_RATE_API_KEY=your_api_key

2. Migrate the database:

bash
Copy code
python manage.py migrate


3. Create a superuser (optional):

bash
Copy code
python manage.py createsuperuser


### Running the Project
1. Start the development server:

bash
Copy code
python manage.py runserver

2. Access the API at http://127.0.0.1:8000/.

### API Endpoints
- Token Generation

POST /token/ - Obtain a new token.
POST /token/refresh/ - Refresh an existing token.

- Account Management

POST /accounts/ - Create a new account.
GET /accounts/<id>/ - Retrieve an account.
PUT /accounts/<id>/ - Update an account.
DELETE /accounts/<id>/ - Delete an account.

- Transaction Management

POST /transactions/ - Create a new transaction.
GET /transactions/ - Retrieve all transactions.

- Account Balance

GET /accounts/<id>/balance/ - Retrieve the account balance.


