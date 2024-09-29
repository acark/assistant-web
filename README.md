# AI Voice Agent for reservations powered by Vapi.ai

## Description
This Django project allows users to manage AI voice assistant for restaurant reservation scenario.The application provides a user-friendly interface for managing reservation process for restaurant's owner.

## Features


## Technologies Used
- Django
- HTML/CSS
- JavaScript
- Bootstrap (optional for styling)

## Installation

### Prerequisites
- Python 3.x
- Django 3.x or higher
- A database (SQLite is used by default)

### Steps
1. Clone the repository
   
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000/`.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Django documentation for guidance on building web applications.
- Bootstrap for responsive design (if used).
