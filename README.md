# AI Quiz (Flask)

A friendly Flask web app featuring a quiz on “Applying AI models in Python,” complete with user authentication, a persistent total score per account, a live leaderboard, a polished UI with smooth transitions, and a 3‑day weather widget powered by OpenWeather’s One Call API 2.5 and Direct Geocoding.[11][12][13]

### Highlights

- Clean UI/UX with a modern theme, glassy navigation, responsive cards, and animated progress bar using a dedicated static/styles.css, avoiding inline styles for maintainability.[14]
- Registration and login with unique usernames, password hashing, protected quiz routes, and a leaderboard that updates whenever you answer correctly.[15][11]
- Weather widget on the home page: type a city, geocode to coordinates, then show a 3‑day forecast with day names, dates, and day/night temperatures using the free One Call API 2.5.[12][13]
- Quiz session system: each play session ends after 20 unique questions, shows a finish page with the final session score, and prompts to view the leaderboard or play again.[16][11]

### Table of contents

- Features and behavior[3]
- Tech stack[17]
- Project structure[14]
- Installation[17]
- Configuration and environment[17]
- Running locally[17]
- Weather integration [free One Call 2.5](12)
- Quiz session flow [20 questions](16)
- UI and CSS styling[14]
- Deployment on PythonAnywhere[10]
- Troubleshooting[12]
- Security notes[15]
- License note[3]

### Features and behavior

- Account system: register with a unique username, login with username and password, and keep an accumulating total_score stored in the database.[11]
- Quiz flow: one random question per page with four shuffled choices, endless question pool overall but capped to 20 per session, updating both the session score and the user’s total_score for the leaderboard.[11][16]
- Session finish: after 20 questions, users are redirected to a completion page displaying the session score and a prompt to visit the leaderboard or start a fresh session.[11]
- Weather widget: enter a city, resolve coordinates via Direct Geocoding, and display the next three daily entries using One Call 2.5 with units=metric and exclude=minutely,hourly,alerts.[13][12]

### Tech stack

- Flask for routing, templating, and WSGI serving in a lightweight, flexible framework that suits rapid iteration.[17]
- Flask‑Login for session management, login protection, and user session lifecycle.[11]
- SQLAlchemy for ORM and clean relational data modeling across SQLite locally and optional MySQL in production.[10]

### Project structure

- Root contains app.py, seed.py, requirements.txt, .env.example, wsgi.py, and the templates and static directories.[10]
- Templates: base.html, index.html, register.html, login.html, quiz.html, quiz_finished.html, and leaderboard.html, all using Jinja inheritance and url_for for static assets.[14]

```bash
project-root/
├─ app.py
├─ seed.py
├─ requirements.txt
├─ .env.example
├─ wsgi.py
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ register.html
│  ├─ login.html
│  ├─ quiz.html
│  ├─ quiz_finished.html
│  └─ leaderboard.html
└─ static/
   └─ styles.css
```

### Installation

- Create a virtual environment, activate it, and install dependencies from requirements.txt to match the runtime used in deployment.[17]
- Copy .env.example to .env and populate values before running the application locally.[17]

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Configuration and environment

- SECRET_KEY secures Flask sessions and must be a long, random, private value; never commit it to source control.[17]
- OWM_API_KEY is required for OpenWeather Direct Geocoding and One Call 2.5 endpoints used by the widget.[13][12]

Example .env:  

```bash
SECRET_KEY=change-this-in-production
OWM_API_KEY=your_openweather_api_key
# DATABASE_URL=sqlite:///app.db
# Optional MySQL (PythonAnywhere):
# DATABASE_URL=mysql+pymysql://username:password@host/dbname
```

### Running locally

- Initialize the database, seed 20 AI‑topic questions, and start the development server to test the full flow.[17]
- Visit the app, register a unique username, log in, answer questions, and check the leaderboard updates.[11]

```bash
# Initialize DB (first run)
python -c "from app import db, app; app.app_context().push(); db.create_all()"

# Seed 20 questions
python seed.py

# Run the app
python app.py
```

### Weather integration (free One Call 2.5)

- Geocoding: use the Direct Geocoding API to convert a city name into coordinates with q, limit=1, and appid parameters.[13]
- Forecast: call One Call API 2.5 at <https://api.openweathermap.org/data/2.5/onecall> with lat, lon, units=metric, exclude=minutely,hourly,alerts, and appid, then render the first three elements from daily.[12]
- The app is configured to use One Call 2.5 to avoid subscription requirements of One Call 3.0, while retaining the same daily fields needed for the UI.[12]

### Quiz session flow (20 questions)

- Session state tracks quiz_count, quiz_correct, and a list of served question IDs to avoid repetition during the 20‑question run.[16]
- After submission, correctness is recorded, total_score is incremented for correct answers, and the session progresses until the cap is reached.[11]
- When the count hits 20 or questions run out, users are redirected to a finish page showing the session score with prompts to view the leaderboard or start a new session.[11]

### Authentication and uniqueness

- Registration uses a unique username with a database unique constraint and a pre‑insert application check for friendly validation.[18]
- Passwords are stored with generate_password_hash and verified with check_password_hash to avoid keeping plaintext credentials.[15]
- Protected routes such as /quiz rely on Flask‑Login’s login_required decorator and login_view redirect behavior.[11]

### UI and CSS styling

- A dedicated static/styles.css provides a responsive layout, glass‑effect navigation, cards, button and input transitions, and a gradient animated background.[14]
- The quiz progress bar is implemented using a CSS custom property --progress and no inline styles, with smooth width transitions and reduced‑motion support.[14]
- On PythonAnywhere, map the /static URL to the static directory in the web app configuration so styles are served correctly in production.[10]

### Deployment on PythonAnywhere

- Create a virtual environment, install requirements, and set environment variables (SECRET_KEY and OWM_API_KEY) in the Web > Environment variables section.[10]
- Ensure your WSGI file imports the Flask app as application and add a static files mapping for /static before reloading the web app.[10]

WSGI example:  

```python
import sys
import os
# project_path = '/home/yourusername/mysite'
# if project_path not in sys.path:
#     sys.path.append(project_path)
from app import app as application
```

### Troubleshooting

- If the weather box shows “City not found or API error,” verify that OWM_API_KEY is loaded by the process and that the app is calling the One Call 2.5 endpoint.[12]
- Test your key using a direct Geocoding call and a One Call 2.5 call with known coordinates to ensure 200 responses before testing via the UI.[13][12]
- If login or session errors occur after deployment, check that SECRET_KEY is set on the host and reload the web app so WSGI picks up the new environment variables.[10]

### Security notes

- Keep SECRET_KEY private and rotate it if ever exposed, using different values for dev and production environments.[17]
- Never hardcode credentials in source files; prefer environment variables locally via .env and host‑level variables in production.[17]

### License note

- Include a LICENSE file if distributing the project publicly and reference it here with a brief statement aligned to your chosen license.[3]

[1](https://gitlab.doc.ic.ac.uk/paas-templates/python-flask-template/-/blob/master/README.md)
[2](https://stackoverflow.com/questions/14415500/common-folder-file-structure-in-flask-app)
[3](https://realpython.com/readme-python-project/)
[4](https://preview.keenthemes.com/flask/metronic/docs/file-structure)
[5](https://flask.palletsprojects.com/en/stable/blueprints/)
[6](https://muneebdev.com/flask-project-structure-best-practices/)
[7](https://vsupalov.com/flask-app-starting-project/)
[8](https://jonnylangefeld.com/blog/python-flask-base-project)
[9](https://citizen-stig.github.io/2015/09/26/flask-project-structure-in-details.html)
[10](https://help.pythonanywhere.com/pages/Flask/)
[11](https://flask-login.readthedocs.io/en/latest/)
[12](https://openweathermap.org/api/one-call-api)
[13](https://openweathermap.org/api/geocoding-api)
[14](https://flask.palletsprojects.com/en/stable/tutorial/templates/)
[15](https://tedboy.github.io/flask/generated/werkzeug.generate_password_hash.html)
[16](https://docs.python.org/3/library/random.html)
[17](https://flask.palletsprojects.com/en/stable/quickstart/)
[18](https://stackoverflow.com/questions/14355499/how-to-model-a-unique-constraint-in-sqlalchemy)
