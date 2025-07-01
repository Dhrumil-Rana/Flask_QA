# Flask QA Application

## Overview
This project is a Flask-based web application that allows users to register, log in, create posts, comment on posts, and manage friends. It utilizes Flask-SocketIO for real-time messaging and Flask-SQLAlchemy for database interactions.

## Project Structure
```
flask_qa_app
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── sockets.py
│   ├── forms.py
│   ├── utils.py
│   └── static
│       └── upload
│       └── css
│        ├── base.css
│        ├── blocked.css
│        ├── friends.css
│        ├── home.css
│        ├── login.css
│        ├── market.css
│        ├── messenger.css
│        ├── nav.css
│        ├── nav2.css
│        ├── post.css
│        ├── profile.css
│        ├── register.css
│        ├── search.css
│── templates
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── blockedposts.html
│   ├── profile.html
│   ├── friends.html
│   ├── messanger.html
│   ├── createpost.html
│   ├── addaccount.html
│   ├── search.html
│   ├── topMarketItems.html
│   └── searchMarketItems.html
├── migrations
├── config.py
├── requirements.txt
├── run.py
├── Password_incrypt.py
├── .env
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask_qa_app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration
- Update the `config.py` file with your database URI and other settings as needed.

## Running the Application
To run the application, execute the following command:
```
python run.py
```
The application will be accessible at `http://127.0.0.1:5000`.

## Usage
- Navigate to the login page to access your account or register a new account.
- Once logged in, you can create posts, comment on them, and manage your friends.
- Use the messaging feature to communicate with your friends in real-time.

## License
This project is licensed under the MIT License. See the LICENSE file for details.