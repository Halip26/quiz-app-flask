# Computer Vision Quiz (Flask)

A friendly Flask web app featuring a quiz on "Computer Vision / Visi Komputer," complete with user authentication, a persistent total score per account, a live leaderboard, a polished UI with smooth transitions, and a 3‑day weather widget powered by OpenWeather's One Call API 2.5 and Direct Geocoding.

## Screenshots

### Home Page

![Home Page Preview](screenshots/ss-beranda.png)
*Home page with Computer Vision learning materials and weather widget*

### Quiz Interface

![Quiz Interface](screenshots/ss_quiz.png)
*Interactive quiz interface with Computer Vision questions*

### Leaderboard

![Leaderboard](screenshots/ss-papan.png)
*Real-time leaderboard showing top performers*

### SignUp

![Leaderboard](screenshots/ss-register.png)
*Real-time leaderboard showing top performers*

### Login

![Leaderboard](screenshots/ss-login.png)
*Real-time leaderboard showing top performers*

> **Note:** Screenshots added on `screenshots/` directory.

---

## Highlights

- **Educational Content:** Interactive learning materials about Computer Vision concepts including Image Processing, Object Detection, Classification, Segmentation, and Feature Extraction
- **Clean UI/UX:** Modern theme with glassy navigation, responsive cards, animated progress bar using a dedicated `static/css/style.css`
- **User Authentication:** Registration and login with unique usernames, password hashing, protected quiz routes, and a leaderboard that updates whenever you answer correctly
- **Weather Widget:** Type a city on the home page, geocode to coordinates, then show a 3‑day forecast with day names, dates, and day/night temperatures using the free One Call API 2.5
- **Quiz System:** 20 unique Computer Vision questions per session, with shuffled answers and progress tracking

---

## Table of Contents

- [Computer Vision Quiz (Flask)](#computer-vision-quiz-flask)
  - [Screenshots](#screenshots)
    - [Home Page](#home-page)
    - [Quiz Interface](#quiz-interface)
    - [Leaderboard](#leaderboard)
    - [SignUp](#signup)
    - [Login](#login)
  - [Highlights](#highlights)
  - [Table of Contents](#table-of-contents)
  - [Features and Behavior](#features-and-behavior)
  - [Tech Stack](#tech-stack)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup Steps](#setup-steps)
  - [Configuration and Environment](#configuration-and-environment)
    - [Getting OpenWeather API Key](#getting-openweather-api-key)
  - [Running Locally](#running-locally)
  - [Weather Integration (free One Call 2.5)](#weather-integration-free-one-call-25)
  - [Quiz Session Flow (20 Questions)](#quiz-session-flow-20-questions)
  - [Authentication and Uniqueness](#authentication-and-uniqueness)
  - [UI and CSS Styling](#ui-and-css-styling)
  - [Deployment on PythonAnywhere](#deployment-on-pythonanywhere)
    - [Steps](#steps)
  - [Troubleshooting](#troubleshooting)
    - [Weather Widget Issues](#weather-widget-issues)
    - [Login/Session Errors](#loginsession-errors)
    - [Database Issues](#database-issues)
    - [CSS Not Loading](#css-not-loading)
  - [Security Notes](#security-notes)
  - [License Note](#license-note)
  - [Contributing](#contributing)
  - [Future Enhancements](#future-enhancements)
  - [Support](#support)

---

## Features and Behavior

- **Account System:** Register with a unique username, login with username and password, and keep an accumulating total_score stored in the database
- **Computer Vision Learning:** Educational content covering core concepts like Image Processing, Object Detection, Image Classification, Segmentation, and practical applications like Face Recognition, Autonomous Vehicles, Medical Imaging, OCR, and Augmented Reality
- **Quiz Flow:** One random question per page with four shuffled choices, 20 questions per session covering topics like CNN, YOLO, OpenCV, Feature Extraction, and real-world Computer Vision applications
- **Session Finish:** After 20 questions, users are redirected to a completion page displaying the session score and a prompt to visit the leaderboard or start a fresh session
- **Weather Widget:** Enter a city, resolve coordinates via Direct Geocoding, and display the next three daily entries using One Call 2.5 with units=metric and exclude=minutely,hourly,alerts
- **Leaderboard:** Real-time ranking of users based on their total accumulated scores from all quiz sessions

---

## Tech Stack

- **Flask** - Routing, templating, and WSGI serving in a lightweight, flexible framework
- **Flask‑Login** - Session management, login protection, and user session lifecycle
- **SQLAlchemy** - ORM and clean relational data modeling across SQLite locally and optional MySQL in production
- **OpenWeather API** - Direct Geocoding and One Call 2.5 for weather data
- **HTML/CSS/Jinja2** - Responsive UI with template inheritance

---

## Project Structure

```
quiz-app-flask/
├─ app.py                    # Main Flask application
├─ seed.py                   # Database seeder with 20 Computer Vision questions
├─ wsgi.py                   # WSGI entry point for deployment
├─ requirements.txt          # Python dependencies
├─ .env.example             # Environment variables template
├─ .env                     # Local environment variables (not in git)
├─ instance/                # SQLite database (auto-created)
├─ templates/               # Jinja2 HTML templates
│  ├─ base.html            # Base template with navigation
│  ├─ index.html           # Home page with CV content & weather
│  ├─ register.html        # User registration form
│  ├─ login.html           # User login form
│  ├─ quiz.html            # Quiz question display
│  ├─ quiz_finished.html   # Session completion page
│  └─ leaderboard.html     # User rankings
├─ static/                  # Static assets
│  └─ css/
│     └─ style.css         # Main stylesheet
└─ screenshots/             # App preview images (add manually)
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenWeather API key (free tier)

### Setup Steps

1. **Clone or download the project**

   ```bash
   cd quiz-app-flask
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env and add your values
   # - SECRET_KEY: Use a long random string
   # - OWM_API_KEY: Get free key from openweathermap.org
   ```

---

## Configuration and Environment

Create a `.env` file in the project root with the following variables:

```bash
# Flask secret key for session security (change this!)
SECRET_KEY=your-very-long-random-secret-key-here

# OpenWeather API key (get free from openweathermap.org)
OWM_API_KEY=your_openweather_api_key_here

# Database URL (optional, defaults to SQLite)
# DATABASE_URL=sqlite:///app.db

# For production with MySQL (e.g., PythonAnywhere):
# DATABASE_URL=mysql+pymysql://username:password@host/dbname
```

### Getting OpenWeather API Key

1. Sign up at [OpenWeatherMap](https://openweathermap.org/)
2. Go to API Keys section
3. Copy your API key to `.env` file

---

## Running Locally

1. **Initialize the database** (first time only)

   ```bash
   python -c "from app import db, app; app.app_context().push(); db.create_all()"
   ```

2. **Seed Computer Vision questions**

   ```bash
   python seed.py
   ```

   This adds 20 Computer Vision questions covering topics like:
   - Image Processing and Classification
   - Object Detection and Segmentation
   - CNNs and Deep Learning in CV
   - OCR and Feature Extraction
   - YOLO and real-time detection
   - Practical applications (Face Recognition, Autonomous Vehicles, Medical Imaging)

3. **Start the development server**

   ```bash
   python app.py
   ```

4. **Access the application**
   - Open browser to `http://localhost:5000`
   - Register a new account
   - Start learning and taking quizzes!

---

## Weather Integration (free One Call 2.5)

The home page includes a weather widget that shows a 3-day forecast for any city:

1. **Geocoding:** Uses Direct Geocoding API to convert city name to coordinates
   - Endpoint: `https://api.openweathermap.org/geo/1.0/direct`
   - Parameters: `q={city_name}&limit=1&appid={API_key}`

2. **Forecast:** Calls One Call API 2.5 for weather data
   - Endpoint: `https://api.openweathermap.org/data/2.5/onecall`
   - Parameters: `lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly,alerts&appid={API_key}`
   - Displays first 3 days from the `daily` array

3. **Why One Call 2.5?**
   - Free tier available (no subscription required)
   - Provides all necessary daily forecast fields
   - One Call 3.0 requires paid subscription

---

## Quiz Session Flow (20 Questions)

1. **Session State:** Tracks `quiz_count`, `quiz_correct`, and served question IDs
2. **Question Selection:** Random questions that haven't been shown in current session
3. **Answer Submission:**
   - Validates correctness
   - Updates session score
   - Increments user's total_score for leaderboard
4. **Completion:** After 20 questions or when questions run out:
   - Shows final session score
   - Offers options to view leaderboard or start new session
5. **Leaderboard Update:** Total scores automatically reflected in real-time rankings

---

## Authentication and Uniqueness

- **Registration:**
  - Username must be unique (database constraint + app validation)
  - Passwords hashed with `generate_password_hash` (never stored as plaintext)
  - User-friendly error messages for duplicate usernames

- **Login:**
  - Password verification with `check_password_hash`
  - Flask-Login manages session cookies
  - Automatic redirect to requested page after login

- **Protected Routes:**
  - `/quiz` requires authentication
  - `@login_required` decorator on protected views
  - Automatic redirect to login page with `login_view`

---

## UI and CSS Styling

- **Responsive Design:** Works on desktop, tablet, and mobile devices
- **Modern Aesthetics:**
  - Glass-effect navigation bar
  - Gradient animated background
  - Card-based layout with shadows and hover effects
  - Smooth transitions and animations

- **Quiz Features:**
  - Animated progress bar using CSS custom properties
  - Color-coded feedback (green for correct, red for incorrect)
  - Reduced-motion support for accessibility

- **Static Files:** All styles in `static/css/style.css` (no inline styles)

---

## Deployment on PythonAnywhere

### Steps

1. **Upload Project:**
   - Upload files via Files tab or git clone

2. **Create Virtual Environment:**

   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```

3. **Configure Web App:**
   - Go to Web tab → Add a new web app
   - Choose Manual configuration → Python 3.10
   - Set Source code and Working directory paths

4. **Set Environment Variables:**
   - Web tab → Environment variables section
   - Add `SECRET_KEY` and `OWM_API_KEY`

5. **Configure WSGI File:**

   ```python
   import sys
   import os
   
   project_home = '/home/yourusername/quiz-app-flask'
   if project_home not in sys.path:
       sys.path.append(project_home)
   
   from app import app as application
   ```

6. **Static Files Mapping:**
   - URL: `/static/`
   - Directory: `/home/yourusername/quiz-app-flask/static/`

7. **Initialize Database:**

   ```bash
   python -c "from app import db, app; app.app_context().push(); db.create_all()"
   python seed.py
   ```

8. **Reload Web App**

---

## Troubleshooting

### Weather Widget Issues

**Problem:** "City not found or API error"

**Solutions:**

- Verify `OWM_API_KEY` is set in environment
- Test API key with direct curl request:

  ```bash
  curl "https://api.openweathermap.org/geo/1.0/direct?q=London&limit=1&appid=YOUR_KEY"
  ```

- Ensure using One Call 2.5 endpoint (not 3.0)
- Check API key activation (may take a few hours after signup)

### Login/Session Errors

**Problem:** Can't login or sessions not persisting

**Solutions:**

- Verify `SECRET_KEY` is set and loaded
- Check Flask session configuration
- Clear browser cookies and try again
- Restart web app after environment variable changes

### Database Issues

**Problem:** Tables not found or migration errors

**Solutions:**

- Run database initialization command
- Delete `instance/app.db` and recreate
- Check SQLAlchemy connection string
- Verify database permissions

### CSS Not Loading

**Problem:** Styles not applied on deployed site

**Solutions:**

- Check static files mapping in PythonAnywhere Web tab
- Verify static file URL in templates uses `url_for('static', filename='...')`
- Clear browser cache
- Check file permissions on server

---

## Security Notes

- **SECRET_KEY:**
  - Use long, random string (minimum 32 characters)
  - Never commit to version control
  - Use different keys for dev and production
  - Rotate if ever exposed

- **API Keys:**
  - Store in environment variables only
  - Add `.env` to `.gitignore`
  - Use separate keys for different environments

- **Passwords:**
  - Hashed using Werkzeug's `generate_password_hash`
  - Never logged or displayed
  - Consider adding password strength requirements

- **Input Validation:**
  - All user inputs sanitized
  - SQL injection prevention via SQLAlchemy ORM
  - XSS prevention via Jinja2 auto-escaping

---

## License Note

This project is provided as-is for educational purposes. Feel free to use, modify, and distribute according to your chosen license.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## Future Enhancements

- [ ] Add timer for each quiz question
- [ ] Implement quiz categories (beginner, intermediate, advanced)
- [ ] Add more Computer Vision topics (GANs, Transformers, 3D Vision)
- [ ] Export quiz results to PDF
- [ ] Add dark mode toggle
- [ ] Multi-language support
- [ ] Add image examples in quiz questions
- [ ] Integration with computer vision libraries demos

---

## Support

For issues, questions, or suggestions:

- Open an issue on the repository
- Check existing documentation
- Review troubleshooting section above

---

**Built with ❤️ using Flask and Computer Vision knowledge**
