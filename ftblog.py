# Importing the Flask module to create a web application
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy


# Creating an instance of the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

posts = [
    {
        'author': 'Jagga Jasoos',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'May 28, 2023'
    },
    {
        'author': 'Sumit Kumar',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'May 29, 2023'
    }
]

# Define your database model(s) here
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

# Defining a route for the root URL ("/") and the "/home" URL
# When a user visits these URLs, the following function will be executed
@app.route("/")
@app.route("/home")
def home():
    # Returning a simple HTML content as the response
    return render_template('home.html', posts=posts, name="Faking Times")
# Defining a route for the "/about" URL
# When a user visits this URL, the following function will be executed
@app.route("/about")
def about():
    # Returning a simple HTML content as the response
    return render_template('about.html', title='About')

# The code inside this block will only run if this script is executed directly
# It will not run if the script is imported as a module

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    
    # Do something with the form data, e.g., save it to a database
    new_user = User(username=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return 'Form submitted successfully!'

# Create the database tables within the application context
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

