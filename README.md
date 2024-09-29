# Restaurant Opening Hours Management

## Description
This Django project allows users to manage the opening hours of restaurants. Users can add, edit, and view the opening hours for each day of the week. The application provides a user-friendly interface for managing time slots and handling closed days.

## Features
- Add and edit opening hours for restaurants.
- Manage time slots for each day of the week.
- Mark days as closed.
- Responsive design for easy use on various devices.

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
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/restaurant-opening-hours.git
   cd restaurant-opening-hours
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`.

## Usage
- Navigate to the opening hours management page.
- Use the form to add or edit opening hours for each restaurant.
- Click "Add Slot" to add additional time slots for a day.
- Mark a day as closed using the checkbox.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Django documentation for guidance on building web applications.
- Bootstrap for responsive design (if used).
