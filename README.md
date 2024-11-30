# Eco Impact Tracker

A web application that helps users track and improve their environmental impact through daily activities, challenges, and community engagement.

## Features

- Carbon footprint calculator and activity tracking
- Daily sustainable living tips
- Monthly eco-challenges with rewards
- Community forum
- Eco-friendly product directory
- Smart device integration

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` file
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

## Project Structure

```
eco_impact_tracker/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── migrations/
├── tests/
├── .env
├── config.py
├── requirements.txt
└── run.py
```

## Development

- Python 3.8+
- Flask web framework
- SQLAlchemy ORM
- Modern frontend with HTML5, CSS3, and JavaScript

## License

MIT License
