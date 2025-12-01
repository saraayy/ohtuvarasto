# ohtuvarasto

A warehouse management system with a web interface.

## Features

- Create and manage multiple warehouses
- Track items and their quantities in each warehouse
- Add, increase, decrease, and remove items
- Edit warehouse names
- Simple web interface built with Flask

## Installation

1. Install dependencies:
```bash
poetry install
```

## Running the Application

### Web Interface

To run the Flask web application:

```bash
# Development mode with debug enabled
cd src
FLASK_DEBUG=true poetry run python app.py
```

Then open your browser to `http://127.0.0.1:5000`

**Note:** For production deployment, use a proper WSGI server like gunicorn instead of the Flask development server.

### Command Line Demo

To run the original command-line demo:

```bash
poetry run python src/index.py
```

## Running Tests

```bash
poetry run pytest
```

## Project Structure

- `src/varasto.py` - Core warehouse storage class
- `src/warehouse_manager.py` - Manages multiple warehouses and items
- `src/app.py` - Flask web application
- `src/templates/` - HTML templates for the web interface
- `src/tests/` - Unit tests