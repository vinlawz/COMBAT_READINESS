# Combat Readiness

## Overview
Combat Readiness is a Django-based web application designed to manage and assess combat readiness.

## Project Structure
```
combat_readiness/
db.sqlite3
decorators.py
manage.py
package.json
.vscode/
    settings.json
combat_readiness/
    __init__.py
    .gitignore
    admins.py
    asgi.py
    decorators.py
    models.py
    serializers.py
    settings.py
    urls.py
    views.py
    wsgi.py
    __pycache__/
        __init__.cpython-312.pyc
        __init__.cpython-313.pyc
        decorators.cpython-313.pyc
        ...
    migrations/
        __init__.py
        ...
    templates/
readiness/
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    urls.py
    views.py
    migrations/
staticfiles/
    admin/
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Django 3.2 or higher

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/combat_readiness.git
    cd combat_readiness
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Apply migrations:
    ```sh
    python manage.py migrate
    ```

4. Run the development server:
    ```sh
    python manage.py runserver
    ```

### Running Tests
To run tests, use the following command:
```sh
python manage.py test
```

## Project Structure
- `combat_readiness/`: Main Django application.
- `readiness/`: Additional Django app for readiness management.
- `staticfiles/`: Static files for the project.
- `templates/`: HTML templates for the project.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
