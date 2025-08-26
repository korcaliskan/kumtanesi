# Aidat Yönetim Sistemi

## Overview

Aidat Yönetim Sistemi, grup aidatlarının takip edildiği web tabanlı bir uygulamadır. Sistem üyelerin aylık aidat ödemelerini, bu aidatlarla yapılan harcamaları ve yatırımları takip eder. Flask framework'ü ve PostgreSQL veritabanı kullanılarak geliştirilmiştir.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **Styling**: Custom CSS with modern design and Bootstrap integration
- **Layout**: Dashboard with sidebar navigation system
- **Forms**: Bootstrap form components for data entry

### Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **Database**: PostgreSQL with models for members, dues, expenses, and investments
- **Authentication**: Session-based login system
- **Request Handling**: Form-based data submission and display

### Data Models
- **Members**: User accounts and member information
- **Dues**: Monthly payment records from members
- **Expenses**: Spending records using collected dues
- **Investments**: Investment tracking from collected funds

### Security and Configuration
- **Environment Variables**: Database connection and session secret configuration
- **Proxy Support**: Werkzeug ProxyFix for deployment behind reverse proxies
- **Authentication**: Login system for authorized access

## External Dependencies

### Database
- **PostgreSQL**: Primary database for all data storage (Neon database integration)

### Python Packages
- **Flask**: Web framework and core application structure
- **Flask-SQLAlchemy**: Database ORM for model management
- **Flask-Session**: Server-side session management
- **Flask-Login**: User authentication management
- **Werkzeug**: WSGI utilities and security functions

### Frontend Libraries
- **Bootstrap 5**: UI framework for responsive design
- **Font Awesome**: Icon library for UI elements

### Development Dependencies
- **Python Logging**: Built-in logging for debugging and monitoring
- **Standard Library**: datetime, os modules for basic functionality