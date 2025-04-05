# MovieWeb App

A Flask-based web application for managing user movie collections. This project is part of a software development program and demonstrates proficiency in Python, Flask, SQLAlchemy, and web development.

## Features

- User management (add, view users)
- Movie collection management (add, view, update, delete movies)
- SQLite database integration
- RESTful API design
- Clean architecture following MVC pattern

## Project Structure

```
movie_web_app/
├── app/                    # Main application package
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   ├── models/            # Database models
│   ├── views/             # View functions and routes
│   ├── controllers/       # Business logic and data manipulation
│   └── __init__.py        # App initialization
├── tests/                 # Test files
├── config/                # Configuration files
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   FLASK_APP=app
   FLASK_ENV=development
   DATABASE_URL=sqlite:///movie_web_app.db
   ```
5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. Run the application:
   ```bash
   flask run
   ```

## Development Progress

### Phase 1: Project Setup and Data Management
- [x] Project structure setup
- [x] Dependencies configuration
- [x] Database models (User, Movie)
- [x] DataManager interface
- [x] SQLiteDataManager implementation

### Phase 2: Web Interface (Coming Soon)
- [ ] Flask application setup
- [ ] User interface templates
- [ ] Route implementations
- [ ] Form handling
- [ ] Error handling

### Phase 3: API Integration (Coming Soon)
- [ ] OMDb API integration
- [ ] Movie data fetching
- [ ] Search functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
