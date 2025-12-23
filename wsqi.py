# wsgi.py
import sys
import os

# add project path as needed:
project_path = "/home/Halip26/quiz-app"
if project_path not in sys.path:
    sys.path.append(project_path)

from app import app as application
