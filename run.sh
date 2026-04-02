#!/bin/bash

# Resume Analyzer - Quick Start Script for macOS/Linux
# This script sets up and runs the modern Resume Analyzer application

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  📄 AI Resume Analyzer - Modern Professional UI"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python detected: $(python3 --version)"
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not available"
    echo "Please ensure pip is installed"
    exit 1
fi

echo "✓ pip detected: $(pip3 --version)"
echo ""

# Install required packages
echo "📦 Installing required packages..."
echo "This may take a few minutes..."
echo ""

pip3 install -r requirements_modern.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install packages"
    exit 1
fi

echo ""
echo "✓ All packages installed successfully!"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Starting Resume Analyzer..."
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Application will open in your default browser"
echo "📍 URL: http://localhost:8501"
echo ""
echo "💡 Tips:"
echo "   - Press Ctrl+C to stop the server"
echo "   - Use 'r' to rerun the app after making changes"
echo "   - Press 'c' to clear terminal"
echo ""

# Run the application
streamlit run resume_analyzer_modern.py
