#!/bin/bash
# Verification script to check all files exist

echo "==================================="
echo "AI Social Media Automation"
echo "Installation Verification"
echo "==================================="
echo ""

APP_DIR="C:\Users\SADANAND\ai-social-media-automation"

echo "Checking core files..."

files=(
    "app.py:Flask Application"
    "requirements.txt:Dependencies"
    ".env.example:Environment Template"
    "README.md:Documentation"
    "SETUP.md:Setup Instructions"
    "templates/base.html:Base Template"
    "templates/index.html:Dashboard"
    "templates/business_setup.html:Business Setup"
    "templates/generate_content.html:Generate Page"
    "templates/content_history.html:History Page"
)

all_exist=true

for file in "${files[@]}"; do
    IFS=':' read -r filename description <<< "$file"
    path="$APP_DIR/$filename"
    
    if [ -f "$path" ]; then
        echo "✅ $filename - $description"
    else
        echo "❌ $filename - MISSING"
        all_exist=false
    fi
done

echo ""
if [ "$all_exist" = true ]; then
    echo "✅ All files verified!"
    echo ""
    echo "Next steps:"
    echo "1. Navigate to: cd C:/Users/SADANAND/ai-social-media-automation"
    echo "2. Create venv: python -m venv venv"
    echo "3. Activate: source venv/bin/activate (Linux/Mac) or venv\Scripts\activate (Windows)"
    echo "4. Install: pip install -r requirements.txt"
    echo "5. Setup .env: Copy .env.example to .env and add API key"
    echo "6. Run: python app.py"
    echo "7. Open: http://127.0.0.1:5000"
else
    echo "❌ Some files are missing. Please check the project directory."
fi
