# AI Social Media Automation Flask Application

A modern, AI-powered Flask web application that helps businesses generate engaging social media content using Google's Gemini API.

## Features

✨ **Smart Content Generation**

- Generate unique social media posts in seconds
- AI-powered content tailored to your business
- Topic, caption, and hashtag generation

📋 **Business Profile Management**

- Store and manage business details (name, industry, tone, audience)
- Customize AI content generation with your business information
- Easy profile editing

🎨 **Modern Dark Dashboard**

- Beautiful dark-themed UI with Tailwind CSS
- Responsive design (works on desktop, tablet, mobile)
- Smooth animations and intuitive navigation

💾 **Content History**

- Track all generated posts
- View, copy, and manage content
- One-click copying to clipboard

🔌 **API Integration**

- Google Gemini AI for content generation
- RESTful API endpoints for programmatic access
- Placeholder function for easy customization

## Technology Stack

- **Backend:** Python Flask
- **Database:** SQLite
- **Frontend:** HTML5, Tailwind CSS
- **AI:** Google Gemini API
- **Configuration:** python-dotenv

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- A free Google Gemini API key

### Step 1: Clone or Download

```bash
# If cloning
git clone <repository-url>
cd ai-social-media-automation

# Or just download and extract the folder
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### Step 5: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# Windows: notepad .env
# macOS/Linux: nano .env
```

In `.env`, set:

```
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 6: Run the Application

```bash
python app.py
```

The app will start at **http://127.0.0.1:5000**

## Usage

### 1. **First Time Setup**

- When you start the app, you'll be redirected to setup
- Enter your business details:
  - Business name
  - Industry
  - Tone of voice
  - Target audience
  - Business description
- Click "Create Profile"

### 2. **Generate Content**

- Go to the "Generate" page
- Review your business details
- Click "Generate Post"
- AI will create a unique post with topic, caption, and hashtags
- Copy the content to use on your social media

### 3. **View History**

- Go to the "History" page
- See all your previously generated posts
- Copy any post to clipboard
- Delete posts you don't need

### 4. **Edit Settings**

- Update your business profile anytime
- Changes will affect future content generation

## Project Structure

```
ai-social-media-automation/
├── app.py                      # Main Flask application
├── database.db                 # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .env                        # Your configuration (create from example)
├── README.md                   # This file
├── static/
│   └── css/
│       └── style.css          # Custom styles (optional)
└── templates/
    ├── base.html              # Base template with navigation
    ├── index.html             # Dashboard home page
    ├── business_setup.html    # Business profile form
    ├── generate_content.html  # Content generation page
    └── content_history.html   # Content history view
```

## API Endpoints

### Web Routes

- `GET /` - Dashboard
- `GET /setup` - Business setup form
- `POST /setup` - Save business profile
- `GET /generate` - Content generation page
- `POST /generate` - Generate new content
- `GET /history` - View content history
- `POST /delete/<id>` - Delete content

### REST API Endpoints

- `POST /api/generate` - Generate content (returns JSON)
- `GET /api/business` - Get current business profile
- `GET /api/content` - Get all content

## Configuration

### Environment Variables

Edit `.env` file to customize:

```
# Flask Settings
FLASK_ENV=development          # development or production
FLASK_DEBUG=True               # True for development
FLASK_HOST=127.0.0.1          # Server host
FLASK_PORT=5000               # Server port

# Gemini API
GEMINI_API_KEY=your_key_here   # Your Google Gemini API key
SECRET_KEY=your_secret_key     # Flask session secret
```

## Troubleshooting

### Issue: "GEMINI_API_KEY not configured"

**Solution:** Make sure you:

1. Created a `.env` file from `.env.example`
2. Added your API key to `.env`
3. Restarted the Flask app

### Issue: "Module not found: google.generativeai"

**Solution:** Install dependencies:

```bash
pip install -r requirements.txt
```

### Issue: Database errors

**Solution:** Delete `database.db` and restart the app:

```bash
rm database.db  # macOS/Linux
del database.db # Windows
python app.py
```

### Issue: Port already in use

**Solution:** Change the port in `.env`:

```
FLASK_PORT=5001
```

## Development

### Running with Auto-Reload

The app runs with `debug=True` by default in development mode, which enables auto-reload when you change files.

### Database Reset

To clear all data and start fresh:

```bash
# Delete the database file
rm database.db

# Restart the app - it will create a fresh database
python app.py
```

### Using the API

Example with curl:

```bash
# Generate content
curl -X POST http://127.0.0.1:5000/api/generate

# Get business profile
curl http://127.0.0.1:5000/api/business

# Get all content
curl http://127.0.0.1:5000/api/content
```

## Customization

### Change Color Theme

Edit `templates/base.html`:

```html
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          primary: "#YOUR_COLOR",
          secondary: "#YOUR_COLOR",
        },
      },
    },
  };
</script>
```

### Modify AI Prompt

Edit the `generate_ai_content()` function in `app.py` to customize how content is generated.

## Tips for Best Results

1. **Specific Business Description:** The more details you provide, the better the AI can tailor content
2. **Consistent Tone:** Choose a tone that matches your brand voice
3. **Detailed Audience:** Specify your target audience for more relevant content
4. **Regenerate:** Click "Generate New" to get different content variations
5. **Customize:** Edit generated content before posting

## Limitations

- Requires active internet connection for Gemini API
- Rate limited by Google's API (free tier has limits)
- Content should be reviewed before posting
- Database limited to SQLite (suitable for small to medium usage)

## License

MIT License - Feel free to use and modify

## Support & Feedback

For issues or suggestions:

1. Check the troubleshooting section
2. Review error messages in Flask console
3. Verify your API key is correct
4. Ensure all dependencies are installed

## Future Enhancements

Potential features for future versions:

- Multiple business profiles
- Scheduled post generation
- Social media platform integrations
- Analytics dashboard
- Custom AI prompts
- Post scheduling
- Team collaboration

---

**Built with ❤️ using Flask and Google Gemini AI**

Last Updated: 2024
