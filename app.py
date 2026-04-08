from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm, CSRFProtect
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from wtforms import StringField, TextAreaField, PasswordField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from config import Config
import bcrypt
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
csrf = CSRFProtect(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Simple user class for admin
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id == app.config.get('ADMIN_USERNAME'):
        return User(user_id)
    return None

# Forms
class BookingForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    destination = SelectField('Destination', choices=[
        ('bromo', 'Mount Bromo Sunrise'),
        ('bali', 'Bali Paradise'),
        ('komodo', 'Komodo Island'),
        ('raja-ampat', 'Raja Ampat'),
        ('lombok', 'Lombok Adventure')
    ], validators=[DataRequired()])
    travel_date = DateField('Travel Date', validators=[DataRequired()])
    guests = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1, max=20)])
    message = TextAreaField('Special Requests', validators=[Length(max=500)])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class NewsletterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

# Sample data
DESTINATIONS = [
    {
        'id': 'bromo',
        'name': 'Mount Bromo',
        'location': 'East Java, Indonesia',
        'image': 'bromo.jpg',
        'price': 299,
        'rating': 4.9,
        'description': 'Experience the magical sunrise over the volcanic landscape of Mount Bromo.'
    },
    {
        'id': 'bali',
        'name': 'Bali Paradise',
        'location': 'Bali, Indonesia',
        'image': 'bali.jpg',
        'price': 449,
        'rating': 4.8,
        'description': 'Discover the island of gods with stunning temples and pristine beaches.'
    },
    {
        'id': 'komodo',
        'name': 'Komodo Island',
        'location': 'East Nusa Tenggara',
        'image': 'komodo.jpg',
        'price': 599,
        'rating': 4.7,
        'description': 'Meet the legendary Komodo dragons and explore pink beaches.'
    },
    {
        'id': 'raja-ampat',
        'name': 'Raja Ampat',
        'location': 'West Papua, Indonesia',
        'image': 'raja-ampat.jpg',
        'price': 899,
        'rating': 5.0,
        'description': 'Dive into the world\'s most biodiverse marine paradise.'
    },
    {
        'id': 'lombok',
        'name': 'Lombok Adventure',
        'location': 'West Nusa Tenggara',
        'image': 'lombok.jpg',
        'price': 349,
        'rating': 4.6,
        'description': 'Trek Mount Rinjani and relax on pristine Gili Islands beaches.'
    }
]

PACKAGES = [
    {
        'id': 'sunrise-tour',
        'name': 'Bromo Sunrise Tour',
        'duration': '2 Days / 1 Night',
        'price': 299,
        'original_price': 399,
        'image': 'package-bromo.jpg',
        'highlights': ['Sunrise viewpoint', 'Jeep adventure', 'Sea of sand', 'Crater visit'],
        'featured': True
    },
    {
        'id': 'bali-escape',
        'name': 'Bali Island Escape',
        'duration': '5 Days / 4 Nights',
        'price': 699,
        'original_price': 899,
        'image': 'package-bali.jpg',
        'highlights': ['Temple tours', 'Rice terraces', 'Beach clubs', 'Spa retreat'],
        'featured': False
    },
    {
        'id': 'komodo-expedition',
        'name': 'Komodo Expedition',
        'duration': '4 Days / 3 Nights',
        'price': 899,
        'original_price': 1099,
        'image': 'package-komodo.jpg',
        'highlights': ['Komodo dragons', 'Pink beach', 'Snorkeling', 'Island hopping'],
        'featured': False
    },
    {
        'id': 'raja-ampat-dive',
        'name': 'Raja Ampat Diving',
        'duration': '7 Days / 6 Nights',
        'price': 1499,
        'original_price': 1899,
        'image': 'package-raja.jpg',
        'highlights': ['10 dive sites', 'Marine life', 'Island tours', 'Local culture'],
        'featured': False
    }
]

TESTIMONIALS = [
    {
        'name': 'Sarah Johnson',
        'location': 'New York, USA',
        'avatar': 'avatar1.jpg',
        'rating': 5,
        'text': 'Absolutely breathtaking experience! The sunrise at Mount Bromo was the most magical moment of my life. The team was professional and made everything seamless.'
    },
    {
        'name': 'Michael Chen',
        'location': 'Singapore',
        'avatar': 'avatar2.jpg',
        'rating': 5,
        'text': 'BromoRise exceeded all my expectations. From booking to the actual trip, everything was perfectly organized. Highly recommend!'
    },
    {
        'name': 'Emma Williams',
        'location': 'London, UK',
        'avatar': 'avatar3.jpg',
        'rating': 5,
        'text': 'A once-in-a-lifetime adventure! The guides were knowledgeable and friendly. The landscapes were out of this world. Will definitely book again!'
    },
    {
        'name': 'David Park',
        'location': 'Seoul, Korea',
        'avatar': 'avatar4.jpg',
        'rating': 5,
        'text': 'The Bali package was incredible. Every detail was taken care of. The accommodations were luxurious and the experiences were authentic.'
    }
]

# Routes
@app.route('/')
def index():
    booking_form = BookingForm()
    newsletter_form = NewsletterForm()
    return render_template('index.html', 
                         destinations=DESTINATIONS,
                         packages=PACKAGES,
                         testimonials=TESTIMONIALS,
                         booking_form=booking_form,
                         newsletter_form=newsletter_form)

@app.route('/destinations')
def destinations():
    return render_template('destinations.html', destinations=DESTINATIONS)

@app.route('/destination/<dest_id>')
def destination_detail(dest_id):
    destination = next((d for d in DESTINATIONS if d['id'] == dest_id), None)
    if not destination:
        flash('Destination not found', 'error')
        return redirect(url_for('destinations'))
    booking_form = BookingForm()
    return render_template('destination_detail.html', destination=destination, booking_form=booking_form)

@app.route('/packages')
def packages():
    return render_template('packages.html', packages=PACKAGES)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            msg = Message(
                subject=f"Contact Form: {form.subject.data}",
                recipients=[app.config['MAIL_USERNAME']],
                body=f"""
New contact form submission:

Name: {form.name.data}
Email: {form.email.data}
Subject: {form.subject.data}

Message:
{form.message.data}
                """
            )
            mail.send(msg)
            flash('Thank you for your message! We will get back to you soon.', 'success')
        except Exception as e:
            flash('Message received! We will contact you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/book', methods=['POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        try:
            # Send confirmation email to customer
            customer_msg = Message(
                subject="Booking Confirmation - BromoRise",
                recipients=[form.email.data],
                html=render_template('emails/booking_confirmation.html',
                                   name=form.name.data,
                                   destination=form.destination.data,
                                   travel_date=form.travel_date.data,
                                   guests=form.guests.data)
            )
            mail.send(customer_msg)
            
            # Send notification to admin
            admin_msg = Message(
                subject=f"New Booking: {form.destination.data}",
                recipients=[app.config['MAIL_USERNAME']],
                body=f"""
New booking received:

Name: {form.name.data}
Email: {form.email.data}
Phone: {form.phone.data}
Destination: {form.destination.data}
Travel Date: {form.travel_date.data}
Guests: {form.guests.data}
Special Requests: {form.message.data}
                """
            )
            mail.send(admin_msg)
            
            flash('Booking submitted successfully! Check your email for confirmation.', 'success')
        except Exception as e:
            flash('Booking received! We will contact you within 24 hours.', 'success')
        return redirect(url_for('index'))
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{error}', 'error')
    return redirect(url_for('index'))

@app.route('/newsletter', methods=['POST'])
def newsletter():
    form = NewsletterForm()
    if form.validate_on_submit():
        flash('Thank you for subscribing to our newsletter!', 'success')
        return redirect(url_for('index'))
    flash('Please enter a valid email address.', 'error')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == app.config.get('ADMIN_USERNAME'):
            stored_hash = app.config.get('ADMIN_PASSWORD_HASH')
            if stored_hash and bcrypt.checkpw(form.password.data.encode('utf-8'), stored_hash.encode('utf-8')):
                user = User(form.username.data)
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

# Utility to generate password hash
def generate_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

if __name__ == '__main__':
    # For development - generate a password hash
    # print(generate_password_hash('your-password-here'))
    app.run(debug=True)
