import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import random

# app.py (atas)
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MAX_QUESTIONS = 20
OWM_API_KEY = os.getenv("OWM_API_KEY")
OWM_GEOCODE_URL = "https://api.openweathermap.org/geo/1.0/direct"
OWM_ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

ID_DAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    total_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512), nullable=False)


class AnswerOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"), nullable=False
    )
    text = db.Column(db.String(256), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)


class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"), nullable=False
    )
    chosen_option_id = db.Column(
        db.Integer,
        db.ForeignKey("answer_option.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_correct = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Helper sesi kuis
def ensure_quiz_session():
    if "quiz_count" not in session:
        session["quiz_count"] = 0
        session["quiz_correct"] = 0
        session["quiz_ids"] = []


def pick_random_question_excluding(ids):
    q = Question.query
    if ids:
        q = q.filter(~Question.id.in_(ids))
    return q.order_by(db.func.random()).first()


# Weather helpers
def dayname_from_utc(ts_utc, tz_offset_seconds):
    dt_local = datetime.utcfromtimestamp(ts_utc) + timedelta(seconds=tz_offset_seconds)
    return ID_DAYS[dt_local.weekday()], dt_local.strftime("%Y-%m-%d")


def get_weather(city_name):
    if not OWM_API_KEY or not city_name:
        return None

    # Geocoding
    geo_params = {"q": city_name, "limit": 1, "appid": OWM_API_KEY}
    g = requests.get(OWM_GEOCODE_URL, params=geo_params, timeout=10)
    if g.status_code != 200:
        return None
    results = g.json()
    if not results:
        return None
    lat = results[0]["lat"]
    lon = results[0]["lon"]

    # One Call 3.0
    oc_params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,alerts",
        "units": "metric",
        "appid": OWM_API_KEY,
    }
    r = requests.get(OWM_ONECALL_URL, params=oc_params, timeout=10)
    if r.status_code != 200:
        return None
    data = r.json()
    tz_offset = data.get("timezone_offset", 0)
    daily = data.get("daily", [])[:3]

    rows = []
    for d in daily:
        dayname, date_str = dayname_from_utc(d["dt"], tz_offset)
        day_temp = round(d["temp"]["day"])
        night_temp = round(d["temp"]["night"])
        rows.append(
            {
                "day": dayname,
                "date": date_str,
                "day_temp": day_temp,
                "night_temp": night_temp,
            }
        )
    return rows


# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    city = ""
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        weather = get_weather(city)
        if not weather:
            flash(
                "Kota tidak ditemukan atau API error atau Halip26 masih mengembangkan fitur ini.",
                "warning",
            )
    today = datetime.utcnow()
    return render_template("index.html", weather=weather, city=city, today=today)


# app.py (route register yang diperbarui)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if password != confirm:
            flash("Konfirmasi kata sandi tidak cocok.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email sudah dipakai.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username sudah dipakai.", "danger")
            return redirect(url_for("register"))

        user = User(
            email=email,
            username=username,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
        # Tandai bahwa akun baru dibuat agar sesi direset setelah login
        session["new_account"] = True
        flash("Registrasi berhasil, silakan login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


# app.py (route login yang diperbarui)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            # Jika akun baru tadi, reset sesi kuis lalu lanjut ke quiz
            if session.pop("new_account", False):
                return redirect(url_for("quiz_reset"))
            return redirect(url_for("quiz"))
        flash("Login gagal.", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "info")
    return redirect(url_for("index"))


def get_random_question():
    ensure_quiz_session()
    remaining = pick_random_question_excluding(session.get("quiz_ids", []))
    if not remaining:
        return None, []
    options = AnswerOption.query.filter_by(question_id=remaining.id).all()
    random.shuffle(options)
    return remaining, options


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    ensure_quiz_session()

    # Jika sudah 20 pertanyaan, langsung ke halaman hasil
    if session["quiz_count"] >= MAX_QUESTIONS:
        return redirect(url_for("quiz_finish"))

    if request.method == "POST":
        qid = int(request.form.get("question_id"))
        chosen = int(request.form.get("option_id"))
        opt = AnswerOption.query.get(chosen)
        is_correct = bool(opt and opt.is_correct)

        # Catat jawaban di DB
        ua = UserAnswer(
            user_id=current_user.id,
            question_id=qid,
            chosen_option_id=chosen,
            is_correct=is_correct,
        )
        db.session.add(ua)

        # Update skor total user (leaderboard) dan skor sesi
        if is_correct:
            current_user.total_score = (current_user.total_score or 0) + 1
            session["quiz_correct"] = session.get("quiz_correct", 0) + 1

        # Update progres sesi (hindari duplikasi ID)
        ids = session.get("quiz_ids", [])
        if qid not in ids:
            ids.append(qid)
        session["quiz_ids"] = ids
        session["quiz_count"] = session.get("quiz_count", 0) + 1

        db.session.commit()

        if session["quiz_count"] >= MAX_QUESTIONS:
            return redirect(url_for("quiz_finish"))
        return redirect(url_for("quiz"))

    # GET: tampilkan pertanyaan berikutnya
    q, options = get_random_question()

    # Jika kehabisan soal sebelum 20 (mis. bank soal < 20), akhiri lebih cepat
    if not q:
        return redirect(url_for("quiz_finish"))

    total_score = current_user.total_score or 0
    progress = session["quiz_count"]
    return render_template(
        "quiz.html",
        question=q,
        options=options,
        total_score=total_score,
        progress=progress,
        max_questions=MAX_QUESTIONS,
    )


@app.route("/quiz/finish")
@login_required
def quiz_finish():
    ensure_quiz_session()
    attempt_correct = session.get("quiz_correct", 0)
    attempt_count = session.get("quiz_count", 0)
    return render_template(
        "quiz_finished.html",
        attempt_correct=attempt_correct,
        attempt_count=attempt_count,
    )


@app.route("/quiz/reset")
@login_required
def quiz_reset():
    session.pop("quiz_count", None)
    session.pop("quiz_correct", None)
    session.pop("quiz_ids", None)
    flash("Sesi kuis direset. Selamat bermain lagi!", "info")
    return redirect(url_for("quiz"))


@app.route("/leaderboard")
def leaderboard():
    top = (
        User.query.order_by(User.total_score.desc(), User.created_at.asc())
        .limit(20)
        .all()
    )
    return render_template("leaderboard.html", users=top)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
