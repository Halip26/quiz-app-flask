# wsgi.py
import sys
import os

# Tambahkan path proyek jika perlu:
project_path = '/home/Halip26/quiz-app-kodland'
if project_path not in sys.path:
    sys.path.append(project_path)

from app import app as application
