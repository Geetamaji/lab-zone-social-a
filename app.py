"""
AI Social Media Automation Flask Application
Main application file with all routes and database functionality
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DATABASE'] = 'database.db'

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Database initialization
def init_db():
    """Initialize SQLite database with required tables"""
    if not os.path.exists(app.config['DATABASE']):
        db = sqlite3.connect(app.config['DATABASE'])
        cursor = db.cursor()
        
        # Business table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS business (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                industry TEXT NOT NULL,
                tone TEXT NOT NULL,
                target_audience TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Content table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                caption TEXT NOT NULL,
                hashtags TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (business_id) REFERENCES business(id)
            )
        ''')
        
        db.commit()
        db.close()

def get_db():
    """Get database connection"""
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def get_business():
    """Get the current business profile (first one in database)"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM business LIMIT 1')
    business = cursor.fetchone()
    db.close()
    return business

def get_business_by_id(business_id):
    """Get business by ID"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM business WHERE id = ?', (business_id,))
    business = cursor.fetchone()
    db.close()
    return business

def generate_ai_content(business):
    """
    Generate social media content using Gemini API
    
    Args:
        business: Business row object containing business details
    
    Returns:
        Dictionary with topic, caption, hashtags or error message
    """
    if not GEMINI_API_KEY:
        return {
            'error': 'GEMINI_API_KEY not configured. Please set it in .env file',
            'topic': 'Sample Topic',
            'caption': 'This is a sample caption. Configure your Gemini API key to generate real content.',
            'hashtags': '#SamplePost #AI #SocialMedia'
        }
    
    try:
        # Import Gemini API
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        # Create prompt for content generation
        prompt = f"""
        You are a professional social media content creator. Generate a compelling social media post 
        based on the following business details:
        
        Business Name: {business['name']}
        Industry: {business['industry']}
        Tone: {business['tone']}
        Target Audience: {business['target_audience']}
        Description: {business['description']}
        
        Generate a social media post with:
        1. TOPIC: A trending or relevant topic (one line)
        2. CAPTION: An engaging caption (2-3 sentences, conversational)
        3. HASHTAGS: Relevant hashtags (space-separated, max 10)
        
        Format your response EXACTLY as:
        TOPIC: [your topic]
        CAPTION: [your caption]
        HASHTAGS: [your hashtags]
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse the response
        topic = ""
        caption = ""
        hashtags = ""
        
        lines = response_text.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('TOPIC:'):
                topic = line.replace('TOPIC:', '').strip()
            elif line.startswith('CAPTION:'):
                caption = line.replace('CAPTION:', '').strip()
                # Collect multi-line captions
                while i + 1 < len(lines) and not lines[i + 1].startswith('HASHTAGS:'):
                    i += 1
                    caption += '\n' + lines[i].strip()
            elif line.startswith('HASHTAGS:'):
                hashtags = line.replace('HASHTAGS:', '').strip()
        
        return {
            'topic': topic or 'Generated Topic',
            'caption': caption or 'Generated Caption',
            'hashtags': hashtags or '#GeneratedContent'
        }
    except ImportError:
        return {
            'error': 'google-generativeai package not installed. Run: pip install google-generativeai',
            'topic': 'Sample Topic',
            'caption': 'Install google-generativeai to generate real content.',
            'hashtags': '#Install #Dependencies'
        }
    except Exception as e:
        return {
            'error': f'Error generating content: {str(e)}',
            'topic': 'Error Topic',
            'caption': 'Failed to generate content. Check your API key and internet connection.',
            'hashtags': '#Error #TryAgain'
        }

# Routes
@app.route('/')
def index():
    """Dashboard - show business profile and recent content"""
    business = get_business()
    
    if not business:
        return redirect(url_for('setup_business'))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM content 
        WHERE business_id = ? 
        ORDER BY created_at DESC 
        LIMIT 5
    ''', (business['id'],))
    recent_content = cursor.fetchall()
    db.close()
    
    return render_template('index.html', business=business, recent_content=recent_content)

@app.route('/setup', methods=['GET', 'POST'])
def setup_business():
    """Setup or edit business profile"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            industry = request.form.get('industry', '').strip()
            tone = request.form.get('tone', '').strip()
            target_audience = request.form.get('target_audience', '').strip()
            description = request.form.get('description', '').strip()
            
            if not all([name, industry, tone, target_audience]):
                flash('All fields are required', 'error')
                return render_template('business_setup.html', business=get_business())
            
            db = get_db()
            cursor = db.cursor()
            
            # Check if business exists
            cursor.execute('SELECT id FROM business LIMIT 1')
            existing = cursor.fetchone()
            
            if existing:
                # Update existing business
                cursor.execute('''
                    UPDATE business 
                    SET name = ?, industry = ?, tone = ?, target_audience = ?, 
                        description = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (name, industry, tone, target_audience, description, existing['id']))
                flash('Business profile updated successfully!', 'success')
            else:
                # Create new business
                cursor.execute('''
                    INSERT INTO business (name, industry, tone, target_audience, description)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, industry, tone, target_audience, description))
                flash('Business profile created successfully!', 'success')
            
            db.commit()
            db.close()
            
            return redirect(url_for('index'))
        
        except Exception as e:
            flash(f'Error saving business profile: {str(e)}', 'error')
    
    business = get_business()
    return render_template('business_setup.html', business=business)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generate social media content page"""
    business = get_business()
    
    if not business:
        flash('Please set up your business profile first', 'warning')
        return redirect(url_for('setup_business'))
    
    content_data = None
    error_message = None
    
    if request.method == 'POST':
        try:
            # Generate content using AI
            content_data = generate_ai_content(business)
            
            # Save to database if no error
            if 'error' not in content_data or not content_data.get('error'):
                db = get_db()
                cursor = db.cursor()
                cursor.execute('''
                    INSERT INTO content (business_id, topic, caption, hashtags)
                    VALUES (?, ?, ?, ?)
                ''', (
                    business['id'],
                    content_data.get('topic', ''),
                    content_data.get('caption', ''),
                    content_data.get('hashtags', '')
                ))
                db.commit()
                db.close()
                flash('Content generated and saved successfully!', 'success')
            else:
                error_message = content_data.get('error', 'Unknown error')
        
        except Exception as e:
            error_message = f'Error: {str(e)}'
            flash(error_message, 'error')
    
    return render_template('generate_content.html', 
                          business=business, 
                          content=content_data,
                          error_message=error_message)

@app.route('/history')
def history():
    """View all generated content history"""
    business = get_business()
    
    if not business:
        flash('Please set up your business profile first', 'warning')
        return redirect(url_for('setup_business'))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM content 
        WHERE business_id = ? 
        ORDER BY created_at DESC
    ''', (business['id'],))
    all_content = cursor.fetchall()
    db.close()
    
    return render_template('content_history.html', content=all_content, business=business)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for generating content (returns JSON)"""
    business = get_business()
    
    if not business:
        return jsonify({'error': 'Business profile not set up'}), 400
    
    try:
        content_data = generate_ai_content(business)
        
        # Save to database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO content (business_id, topic, caption, hashtags)
            VALUES (?, ?, ?, ?)
        ''', (
            business['id'],
            content_data.get('topic', ''),
            content_data.get('caption', ''),
            content_data.get('hashtags', '')
        ))
        db.commit()
        db.close()
        
        return jsonify(content_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/business', methods=['GET'])
def api_get_business():
    """API endpoint to get current business profile"""
    business = get_business()
    
    if not business:
        return jsonify({'error': 'No business profile found'}), 404
    
    return jsonify({
        'id': business['id'],
        'name': business['name'],
        'industry': business['industry'],
        'tone': business['tone'],
        'target_audience': business['target_audience'],
        'description': business['description'],
        'created_at': business['created_at'],
        'updated_at': business['updated_at']
    })

@app.route('/api/content', methods=['GET'])
def api_get_content():
    """API endpoint to get all content"""
    business = get_business()
    
    if not business:
        return jsonify({'error': 'No business profile found'}), 404
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT * FROM content 
        WHERE business_id = ? 
        ORDER BY created_at DESC
    ''', (business['id'],))
    content_rows = cursor.fetchall()
    db.close()
    
    content_list = [
        {
            'id': row['id'],
            'topic': row['topic'],
            'caption': row['caption'],
            'hashtags': row['hashtags'],
            'created_at': row['created_at']
        }
        for row in content_rows
    ]
    
    return jsonify(content_list)

@app.route('/delete/<int:content_id>', methods=['POST'])
def delete_content(content_id):
    """Delete a piece of content"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM content WHERE id = ?', (content_id,))
        db.commit()
        db.close()
        flash('Content deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting content: {str(e)}', 'error')
    
    return redirect(url_for('history'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# Application entry point
if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run Flask development server
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(
        host=os.getenv('FLASK_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=debug_mode
    )
