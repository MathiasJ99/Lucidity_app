from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from db import db
from routes_main import main
from routes_apply import apply
from models import Tags
import csv

from werkzeug.utils import secure_filename
# Load env variables
load_dotenv()

# Create an instance of the Flask class
app = Flask(__name__)

#db configurations

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', f"sqlite:///{os.path.join(app.instance_path, 'Test.db')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

csv_file_path = os.path.join(app.root_path, 'static', 'data', 'Tags.csv')

# Initialize database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db) 

# Register Blueprints
app.register_blueprint(main)
app.register_blueprint(apply)

# Function to load data from CSV
def load_tags_from_csv(csv_path):
        # Check if data already exists to prevent duplicates
        if not Tags.query.first():
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row if CSV has one

                for row in reader:
                    new_tag = Tags(category=row[1], tags=row[2])
                    db.session.add(new_tag)

            db.session.commit()
            print("Tags loaded successfully.")


# Create database tables
with app.app_context():
    db.create_all()
    db.session.query(Tags).delete()
    load_tags_from_csv(csv_file_path)

    print("Database tables created in Test.db")

if __name__ == '__main__':
    app.run(port=4242, debug=True)
