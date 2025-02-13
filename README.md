# Vic's Royal Beauty - E-commerce Platform

## Overview
Vic's Royal Beauty is a sophisticated e-commerce platform specializing in premium hair products. Built with Django and modern web technologies, this platform offers a seamless shopping experience with a focus on user experience and performance.

## Features
- **User Authentication & Profiles**
  - Secure user registration and login
  - Personal wishlists
  - Order history tracking
  - Profile management

- **Product Management**
  - Categorized product browsing
  - Advanced search functionality
  - Dynamic filtering options
  - Detailed product pages with images
  - Sale and discount management

- **Shopping Experience**
  - Intuitive shopping cart
  - Secure checkout process
  - Real-time stock updates
  - Wishlist functionality
  - Special offers section

- **Admin Features**
  - Comprehensive admin dashboard
  - Product inventory management
  - Order processing
  - Customer management
  - Sales analytics

- **Additional Features**
  - Responsive design
  - Blog section with hair care tips
  - Newsletter subscription
  - Customer support integration
  - WhatsApp business integration

## Technology Stack
- **Backend**: Django 5.1.4
- **Database**: PostgreSQL
- **Frontend**: 
  - HTML5
  - CSS3 (Material Design)
  - JavaScript
  - Tailwind CSS
- **Authentication**: Django Authentication System
- **File Storage**: WhiteNoise
- **Deployment**: Gunicorn

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/hair_ecomm.git
cd hair_ecomm
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create a superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## Environment Variables
Create a `.env` file with the following variables:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=your_database_url
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details

## Contact
- Website: [Vic's Royal Beauty](https://vicsroyalbeauty.com)
- Email: support@vicsroyalbeauty.com
- WhatsApp: [Business Contact]

## Acknowledgments
- Material Design Components
- Django Community
- All contributors who have helped shape this project

---
**Note**: This project is continuously being improved. Feel free to report issues or suggest improvements. 