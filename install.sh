#!/bin/bash

echo "🔧 Setting up Python virtual environment..."

python3 -m venv venv
source venv/bin/activate

echo "📦 Installing requirements..."
pip install -r requirements.txt

echo "✅ All requirements installed."
echo "🎉 To activate your environment later, run: source venv/bin/activate"