# KumTanesi AI Assistant

## Overview

KumTanesi is a Turkish-speaking AI chatbot built with Flask and OpenAI's GPT-5 model. The application provides a web-based chat interface where users can interact with an AI assistant that responds exclusively in Turkish. The system features a clean, responsive UI with real-time messaging capabilities and session-based conversation history management.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **Styling**: Custom CSS with dark theme support and Bootstrap integration
- **JavaScript**: Vanilla JavaScript with ES6 classes for chat functionality
- **Real-time Updates**: AJAX-based messaging system with loading indicators and error handling

### Backend Architecture
- **Web Framework**: Flask with session management using filesystem-based storage
- **Agent System**: Modular AI agent class (`KumTanesiAgent`) that encapsulates OpenAI API interactions
- **Session Management**: Flask-Session for maintaining conversation history across requests
- **Request Handling**: RESTful API endpoints for chat interactions with JSON responses

### Data Models
- **Message Structure**: Dataclass-based models for chat messages and conversation sessions
- **Session Storage**: In-memory conversation history with configurable message limits (8 recent messages)
- **Conversation Context**: Automatic context management for maintaining coherent AI responses

### AI Integration
- **Model**: OpenAI GPT-5 with Turkish language system prompts
- **Context Management**: Rolling conversation window to maintain relevant chat history
- **Response Configuration**: Tuned temperature and penalty settings for natural Turkish responses

### Security and Configuration
- **Environment Variables**: Secure API key management and session secret configuration
- **Proxy Support**: Werkzeug ProxyFix for deployment behind reverse proxies
- **Error Handling**: Comprehensive error handling with user-friendly Turkish error messages

## External Dependencies

### Third-party Services
- **OpenAI API**: GPT-5 model for AI chat responses (requires `OPENAI_API_KEY` environment variable)

### Python Packages
- **Flask**: Web framework and core application structure
- **Flask-Session**: Server-side session management
- **OpenAI**: Official OpenAI Python client library
- **Werkzeug**: WSGI utilities and proxy handling

### Frontend Libraries
- **Bootstrap 5**: UI framework with Replit dark theme integration
- **Font Awesome**: Icon library for UI elements
- **Replit Bootstrap Theme**: Custom dark theme CSS from Replit CDN

### Development Dependencies
- **Python Logging**: Built-in logging for debugging and monitoring
- **Standard Library**: dataclasses, typing, datetime, and os modules