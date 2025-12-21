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
OWM_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

ID_DAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


# models
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
def get_weather(city_name):
    if not OWM_API_KEY or not city_name:
        return None

    try:
        # Geocoding
        geo_params = {"q": city_name, "limit": 1, "appid": OWM_API_KEY}
        g = requests.get(OWM_GEOCODE_URL, params=geo_params, timeout=10)
        if g.status_code != 200:
            print(f"Geocoding error: {g.status_code} - {g.text}")
            return None
        results = g.json()
        if not results:
            print("City not found in geocoding")
            return None
        lat = results[0]["lat"]
        lon = results[0]["lon"]

        forecast_params = {
            "lat": lat,
            "lon": lon,
            "units": "metric",
            "appid": OWM_API_KEY,
        }
        r = requests.get(OWM_FORECAST_URL, params=forecast_params, timeout=10)
        if r.status_code != 200:
            print(f"Forecast error: {r.status_code} - {r.text}")
            return None

        data = r.json()
        forecast_list = data.get("list", [])
        if not forecast_list:
            return None

        from collections import defaultdict

        daily_data = defaultdict(list)

        for item in forecast_list:
            dt = datetime.fromtimestamp(item["dt"])
            date_key = dt.date()
            daily_data[date_key].append({"temp": item["main"]["temp"], "hour": dt.hour})

        rows = []
        for date_key in sorted(daily_data.keys())[:3]:
            temps = daily_data[date_key]

            # cari suhu siang (12:00-15:00) dan malam (21:00-03:00)
            day_temps = [t["temp"] for t in temps if 12 <= t["hour"] <= 15]
            night_temps = [
                t["temp"] for t in temps if t["hour"] >= 21 or t["hour"] <= 3
            ]

            # jika tidak ada data spesifik, gunakan max/min dari hari itu
            day_temp = (
                round(max(day_temps))
                if day_temps
                else round(max(t["temp"] for t in temps))
            )
            night_temp = (
                round(min(night_temps))
                if night_temps
                else round(min(t["temp"] for t in temps))
            )

            # nama hari dalam bahasa
            dayname = ID_DAYS[date_key.weekday()]
            date_str = date_key.strftime("%Y-%m-%d")

            rows.append(
                {
                    "day": dayname,
                    "date": date_str,
                    "day_temp": day_temp,
                    "night_temp": night_temp,
                }
            )

        return rows

    except Exception as e:
        print(f"Weather API error: {e}")
        return None


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
                "Kota tidak ditemukan atau terjadi error. Pastikan nama kota benar dan API key aktif.",
                "warning",
            )
    today = datetime.utcnow()
    return render_template("index.html", weather=weather, city=city, today=today)


# app.py (route register yang diperbarui)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Email: selalu disimpan dalam lowercase (case-insensitive)
        email = request.form.get("email", "").strip().lower()
        # Username: disimpan sesuai input user (case-sensitive)
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
        # tandai bahwa akun baru dibuat agar sesi direset setelah login
        session["new_account"] = True
        flash("Registrasi berhasil, silakan login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


# app.py (route login yang diperbarui)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_or_username = request.form.get("email_or_username", "").strip()
        password = request.form.get("password", "")
        
        # Cek apakah input adalah email (mengandung @) atau username
        if "@" in email_or_username:
            # Login dengan email (CASE-INSENSITIVE: selalu lowercase)
            user = User.query.filter_by(email=email_or_username.lower()).first()
        else:
            # Login dengan username (CASE-SENSITIVE: harus sesuai huruf besar/kecil)
            user = User.query.filter_by(username=email_or_username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            # Jika akun baru tadi, reset sesi kuis lalu lanjut ke quiz
            if session.pop("new_account", False):
                return redirect(url_for("quiz_reset"))
            return redirect(url_for("quiz"))
        flash("Login gagal. Periksa email/username dan password kamu.", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    # Clear quiz session data to prevent leakage to next user
    session.pop("quiz_count", None)
    session.pop("quiz_correct", None)
    session.pop("quiz_ids", None)
    flash("Kamu telah logout.", "info")
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

    # jika sudah 20 pertanyaan, langsung ke halaman hasil
    if session["quiz_count"] >= MAX_QUESTIONS:
        return redirect(url_for("quiz_finish"))

    # Cek leaderboard HANYA jika kuis baru dimulai (quiz_count == 0)
    # Jika user sedang di tengah kuis (quiz_count > 0), jangan dialihkan.
    if session["quiz_count"] == 0:
        top_users = (
            User.query.order_by(User.total_score.desc(), User.created_at.asc())
            .limit(20)
            .all()
        )
        if any(u.id == current_user.id for u in top_users) and (current_user.total_score or 0) > 0:
            return redirect(url_for("quiz_finish"))

    if request.method == "POST":
        qid = int(request.form.get("question_id"))
        chosen = int(request.form.get("option_id"))
        opt = AnswerOption.query.get(chosen)
        is_correct = bool(opt and opt.is_correct)

        # catat jawaban di DB
        ua = UserAnswer(
            user_id=current_user.id,
            question_id=qid,
            chosen_option_id=chosen,
            is_correct=is_correct,
        )
        db.session.add(ua)

        # update skor total user (leaderboard) dan skor sesi
        if is_correct:
            current_user.total_score = (current_user.total_score or 0) + 1
            session["quiz_correct"] = session.get("quiz_correct", 0) + 1

        # update progres sesi (hindari duplikasi ID)
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

    # jika kehabisan soal sebelum 20 (mis. bank soal < 20), akhiri lebih cepat
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
    # If there is an active session with progress, show that.
    # Otherwise (e.g. redirected from start because already on leaderboard), show total score.
    if session.get("quiz_count", 0) > 0:
        attempt_correct = session.get("quiz_correct", 0)
        attempt_count = session.get("quiz_count", 0)
    else:
        attempt_correct = current_user.total_score
        attempt_count = MAX_QUESTIONS

    ensure_quiz_session() # Re-ensure session (though we might not need it if we are done)
    
    return render_template(
        "quiz_finished.html",
        attempt_correct=attempt_correct,
        attempt_count=attempt_count,
    )


@app.route("/quiz/reset")
@login_required
def quiz_reset():
    # Check if user is in leaderboard (top 20)
    top_users = (
        User.query.order_by(User.total_score.desc(), User.created_at.asc())
        .limit(20)
        .all()
    )
    
    in_leaderboard = any(u.id == current_user.id for u in top_users) and (current_user.total_score or 0) > 0
    
    if in_leaderboard:
        current_user.total_score = 0
        db.session.commit()
        flash("Skor leaderboard kamu direset untuk bermain kembali.", "warning")

    session.pop("quiz_count", None)
    session.pop("quiz_correct", None)
    session.pop("quiz_ids", None)

    if not in_leaderboard:
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
