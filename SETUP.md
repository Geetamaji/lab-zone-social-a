# AI Social Media Automation - Setup Instructions

## Quick Start (5 Minutes)

### 1. Open Command Prompt or Terminal

```bash
cd C:\Users\SADANAND\ai-social-media-automation
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup .env File

```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your Gemini API key
# Get key from: https://makersuite.google.com/app/apikey
```

### 5. Run the App

```bash
python app.py
```

### 6. Open in Browser

```
http://127.0.0.1:5000
```

## File Checklist

✅ Core Application Files

- app.py (Flask application - 14,548 bytes)
- requirements.txt (Dependencies)
- .env.example (Configuration template)
- README.md (Complete documentation)

✅ Template Files (HTML)

- templates/base.html (Base layout)
- templates/index.html (Dashboard)
- templates/business_setup.html (Business form)
- templates/generate_content.html (Content generation)
- templates/content_history.html (History view)

✅ Directory Structure

- static/css/ (For custom CSS)

## What Each Component Does

### app.py

- Main Flask application
- Database management (SQLite)
- Routes: Dashboard, Setup, Generate, History
- Gemini API integration
- Form handling and validation

### Templates

- **base.html**: Navigation, footer, flash messages
- **index.html**: Dashboard with recent posts
- **business_setup.html**: Business profile form
- **generate_content.html**: Content generation interface
- **content_history.html**: View all generated posts

### Database

- Auto-created on first run (database.db)
- Two tables: business, content
- SQLite format (no external database needed)

## Features Overview

1. **Business Profile**
   - Store business name, industry, tone, target audience
   - Easy editing
   - Used for AI content generation

2. **Content Generation**
   - AI-powered (Google Gemini)
   - Generates: Topic, Caption, Hashtags
   - One-click generation
   - Copy to clipboard

3. **History Tracking**
   - All generated posts saved
   - View, copy, delete posts
   - Export-ready format

4. **Dark Modern UI**
   - Tailwind CSS
   - Responsive design
   - Beautiful dark theme
   - Emoji-enhanced interface

## API Keys & Configuration

### Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key
5. Paste into .env file

### Environment Variables (.env)

```
GEMINI_API_KEY=your_key_here
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

## Troubleshooting

### Port Already in Use

Change port in .env:

```
FLASK_PORT=5001
```

### Missing Dependencies

```bash
pip install -r requirements.txt --upgrade
```

### API Key Issues

- Check .env file has correct key
- Verify API key is active on Google AI Studio
- Restart Flask app after changing key

### Database Issues

```bash
# Delete and recreate database
del database.db
python app.py
```

## Next Steps

1. ✅ Setup complete
2. 🌐 Open http://127.0.0.1:5000
3. ⚙️ Create business profile
4. ✨ Generate first post
5. 📚 View history
6. 📋 Copy and use on social media

## Support

For detailed information, see README.md

Enjoy automating your social media! 🚀
