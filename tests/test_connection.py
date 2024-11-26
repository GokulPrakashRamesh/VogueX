from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import text  # Import the text function

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/fashion'
db = SQLAlchemy(app)

try:
    with app.app_context():
        # Use the text() function to wrap the raw SQL
        db.session.execute(text('SELECT 1'))
    print("Connected to MySQL successfully!")
except Exception as e:
    print("Connection failed:", e)
