# Malanga1 Company Ltd | Premium Real Estate Platform

A sophisticated, high-end real estate storefront and sales management CRM built for **Malanga1 Company Ltd**. This platform solves accommodation challenges in Northern Ghana through verified, litigation-free land security and modern architectural excellence.

![Malanga1 Premium Storefront](https://github.com/Abdul6619977/malanga-real-estate/raw/main/static/images/hero_preview.jpg)

## 💎 Core Features

### 🏢 Premium Property Storefront
- **Advanced Filtering**: Search by location, property type, price range, and bedroom count.
- **Interactive Galleries**: High-resolution multi-image showcases for every listing.
- **Secure Inquiries**: Integrated documentation request pipeline for potential buyers.

### 📊 Sales Management CRM (Admin)
- **Advanced Dashboard**: Real-time sales analytics, inventory value tracking, and conversion metrics.
- **Inventory Control**: Full CRUD management of property listings and media assets.
- **Lead Pipeline**: Comprehensive management of buyer inquiries with status tracking (New → Negotiating → Sold).
- **Staff Provisioning**: Secure multi-admin access control for team members.

## 🛠️ Technology Stack
- **Backend**: Django (Python)
- **Database**: SQLite (Development)
- **Admin Theme**: Jazzmin (Premium Professional UI)
- **Frontend**: Custom Vanilla CSS (Luxury Theme), HTML5, JavaScript
- **Fonts**: Outfit & Inter (Google Fonts)

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Virtualenv

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Abdul6619977/malanga-real-estate.git
   cd malanga-real-estate
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django django-jazzmin
   ```

4. **Initialize Database**:
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## 🛡️ Security Note
Ensure you set the following environment variables in production:
- `DJANGO_SECRET_KEY`: Your private production key.
- `DJANGO_DEBUG`: Set to `False`.
- `DJANGO_ALLOWED_HOSTS`: Your domain list.

---
*Built for generations by Malanga1 Company Ltd. CEO: Wumpini Iliasu (Mr. Malanga)*
