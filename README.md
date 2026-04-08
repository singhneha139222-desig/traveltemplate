# BromoRise - Premium Travel Booking Website

A modern, responsive travel booking website built with Flask (Python) and HTML/CSS/JavaScript. Features glassmorphism UI design, smooth animations, and a complete booking system.

![BromoRise Preview](https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=600&fit=crop)

## ✨ Features

### Frontend
- **Modern Glassmorphism Design** - Premium UI with glass effects, blur, and transparency
- **Fully Responsive** - Mobile, tablet, and desktop optimized
- **Smooth Animations** - Scroll-triggered animations, hover effects, parallax
- **Interactive Carousels** - Touch-friendly destination and testimonial sliders
- **Loading Animations** - Beautiful page loader with spinner

### Backend
- **Flask Framework** - Python web framework with Jinja2 templating
- **Secure Authentication** - bcrypt password hashing, secure sessions
- **CSRF Protection** - Flask-WTF CSRF tokens on all forms
- **Email Integration** - Flask-Mail for booking confirmations
- **Form Validation** - Server-side and client-side validation

### Pages
- **Home** - Hero section, destinations, packages, testimonials, booking form
- **Destinations** - Grid view of all destinations with filtering
- **Destination Detail** - Individual destination pages with booking
- **Packages** - Travel package listings with pricing
- **About** - Company story, values, and team
- **Contact** - Contact form with map
- **Admin Dashboard** - Booking management (login required)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "c:\Users\rahul\Code\N\Travel Template"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   Mac/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   
   Copy `.env.example` to `.env` and update the values:
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` with your settings:
   ```
   SECRET_KEY=your-super-secret-key-here
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ADMIN_PASSWORD_HASH=your-bcrypt-hash
   ```

6. **Generate admin password hash**
   ```python
   python -c "import bcrypt; print(bcrypt.hashpw(b'your-password', bcrypt.gensalt()).decode())"
   ```
   Copy the output to `ADMIN_PASSWORD_HASH` in `.env`

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
Travel Template/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── templates/
│   ├── base.html         # Base template with navbar/footer
│   ├── index.html        # Homepage
│   ├── destinations.html # Destinations listing
│   ├── destination_detail.html
│   ├── packages.html     # Packages listing
│   ├── about.html        # About page
│   ├── contact.html      # Contact page
│   ├── login.html        # Admin login
│   ├── admin/
│   │   └── dashboard.html
│   ├── errors/
│   │   ├── 404.html
│   │   └── 500.html
│   └── emails/
│       └── booking_confirmation.html
└── static/
    ├── css/
    │   └── style.css     # Main stylesheet
    ├── js/
    │   └── main.js       # JavaScript functionality
    └── images/           # Image assets (add your own)
```

## 🎨 Customization

### Colors
Edit CSS variables in `static/css/style.css`:
```css
:root {
    --primary: #FF6B35;        /* Orange accent */
    --secondary: #1A1A2E;      /* Dark blue */
    --dark: #0F0F1A;           /* Near black */
    --light: #FFFFFF;          /* White */
}
```

### Images
Replace placeholder Unsplash images with your own:
- Add images to `static/images/`
- Update image paths in templates
- Recommended sizes:
  - Hero: 1920x1080
  - Cards: 400x500
  - Gallery: 800x600

### Content
- Destinations/Packages: Edit `DESTINATIONS` and `PACKAGES` in `app.py`
- Testimonials: Edit `TESTIMONIALS` in `app.py`
- Contact info: Update in templates

## 🔐 Security Features

- **CSRF Protection** - All forms protected against CSRF attacks
- **Password Hashing** - bcrypt with salt for admin password
- **Secure Sessions** - HTTPOnly, SameSite cookies
- **Input Validation** - Server-side validation with WTForms
- **XSS Prevention** - Jinja2 auto-escaping

## 📧 Email Setup

For Gmail:
1. Enable 2-factor authentication
2. Create an App Password
3. Use the app password in `.env`

For other providers, update `MAIL_SERVER` and `MAIL_PORT` in config.

## 🌐 Deployment

### Render
1. Create a new Web Service
2. Connect your repository
3. Set environment variables
4. Deploy

### Heroku
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Add `gunicorn` to requirements.txt
3. Deploy via Git

### VPS (Ubuntu)
1. Install Python, nginx, supervisor
2. Set up virtual environment
3. Configure nginx as reverse proxy
4. Use supervisor to manage the app

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome for Android)

## 🙏 Credits

- **Fonts**: [Google Fonts](https://fonts.google.com/) - Playfair Display, Poppins
- **Icons**: [Font Awesome](https://fontawesome.com/)
- **Images**: [Unsplash](https://unsplash.com/)
- **Avatars**: [Random User](https://randomuser.me/)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Built with ❤️ for travel enthusiasts
