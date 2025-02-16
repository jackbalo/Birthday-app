# Birthday Diaries App
Almost Final

# Flask Authentication App  

A simple Flask web application with authentication, password reset functionality, and email integration using Flask-Mail to manage birthdays of friends.

## Features  
- User authentication (login, logout, and registration)  
- Password reset via email  
- Flask-Mail for email functionality  
- Flask-Migrate for database migrations  
- Flask-Login for user session management  

## Tech Stack  
- Python (Flask)  
- Flask-Mail, Flask-Migrate, Flask-Login  
- SQLite (or any SQL database of choice)  

## Installation & Setup  

1. **Clone the Repository**  
   ```sh
   git clone https://github.com/jackbalo/flask-auth-app.git
   cd flask-auth-app

2. Create and Activate Virtual Environment

python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install Dependencies

pip install -r requirements.txt


4. Set Up Environment Variables
Create a .env file and add:

SECRET_KEY=your_secret_key
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_password
MAIL_USE_TLS=True



Database Initialization

1. Run Migrations

flask db init  
flask db migrate -m "Initial migration"  
flask db upgrade



Running the App

flask run

The app will be accessible at http://127.0.0.1:5000/.

Project Structure

flask-auth-app/
│── app/
│   │── __init__.py
│   │── routes.py
│   │── models.py
│   │── forms.py
│   ├── templates/
│   ├── static/
│── migrations/
│── .env
│── config.py
│── requirements.txt
│── README.md
│── run.py

Contribution

Feel free to fork this repository and contribute via pull requests.

License

This project is licensed under the MIT License.
