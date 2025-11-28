# E-commerce Store Assignment

This project implements a simple e-commerce store API with cart management, checkout, and a coupon generation system based on the Nth order logic.

## Features

- **Cart Management**: Add items to a user's cart.
- **Checkout**: Process orders and apply discount coupons.
- **Coupon System**: 
    - Generates a 10% discount coupon for every *Nth* order (configurable, default N=5).
    - Coupons are valid for a single use and expire if not used before the next Nth order.
- **Analytics**: Admin API to view store statistics (total orders, items, revenue, discounts).
- **In-Memory Store**: Data is stored in memory as per the assignment requirements.

## Tech Stack

I have chosen **Django** and **Django REST Framework** for this assignment.

- Python 3.13
- Django & Django REST Framework
- `drf-spectacular` for API Documentation

## Setup & Running

### Option 1: Using `uv` (Recommended)

If you have [uv](https://github.com/astral-sh/uv) installed:

```bash
# Sync dependencies and create virtual environment automatically
uv sync

# Run the server
uv run manage.py runserver
```

### Option 2: Using Standard `venv` & `pip`

If you prefer standard Python tools:

1.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the server**:
    ```bash
    python manage.py runserver
    ```

3.  **Access API Documentation**:
    Open your browser and navigate to:
    - Swagger UI: `http://127.0.0.1:8000/api/docs/`
    - Schema: `http://127.0.0.1:8000/api/schema/`

## API Endpoints

### Store
- `POST /api/store/cart/`: Add item to cart.
- `GET /api/store/cart/`: Get user's cart.
- `POST /api/store/checkout/`: Checkout and place order.

### Admin
- `GET /api/store/admin/analytics/`: View store analytics.
- `POST /api/store/admin/generate-coupon/`: Generate a discount coupon (if eligible).

## Running Tests

Run the unit tests to verify functionality:

```bash
python manage.py test
```

To check test coverage:

```bash
coverage run manage.py test
coverage report -m
```

## Assumptions

- **Data Persistence**: The application uses an in-memory dictionary (`STORE`) to store data. **Data will be lost when the server restarts.**
- **Coupon Logic**: Only one active coupon exists at a time. Generating a new coupon (when eligible) expires the previous one.
