import sys, os

# This tells DreamHost to look in the current directory for the app
sys.path.append(os.getcwd())

# Import the Flask app
from app import app as application

if __name__ == "__main__":
    application.run()