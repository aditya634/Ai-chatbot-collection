#!/usr/bin/env python3
"""
Setup script for AI Chatbot Collection
Helps users set up the environment and dependencies
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def main():
    print("🤖 AI Chatbot Collection Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not os.path.exists("chatbot_env"):
        if not run_command("python -m venv chatbot_env", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists!")
    
    # Activate virtual environment and install dependencies
    if sys.platform.startswith('win'):
        activate_script = "chatbot_env\\Scripts\\activate"
        pip_command = "chatbot_env\\Scripts\\pip"
    else:
        activate_script = "source chatbot_env/bin/activate"
        pip_command = "chatbot_env/bin/pip"
    
    # Install requirements
    if not run_command(f"{pip_command} install -r requirements.txt", "Installing Python packages"):
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. For Ollama chatbots:")
    print("   - Install Ollama from https://ollama.com/download")
    print("   - Run: ollama pull qwen2.5:7b-instruct")
    print("   - Start server: ollama serve")
    print("\n2. For Gemini chatbot:")
    print("   - Get API key from https://makersuite.google.com/app/apikey")
    print("   - Replace YOUR_API_KEY in ChatBot_api.py")
    print("\n3. Run the applications:")
    
    if sys.platform.startswith('win'):
        print("   - Terminal chatbot: chatbot_env\\Scripts\\python ChatBot_api.py")
        print("   - Local chatbot: chatbot_env\\Scripts\\streamlit run ChatBot_Local_Host.py")
        print("   - Scraper bot: chatbot_env\\Scripts\\streamlit run ChatBot_scraper_app.py")
    else:
        print("   - Terminal chatbot: chatbot_env/bin/python ChatBot_api.py")
        print("   - Local chatbot: chatbot_env/bin/streamlit run ChatBot_Local_Host.py")
        print("   - Scraper bot: chatbot_env/bin/streamlit run ChatBot_scraper_app.py")

if __name__ == "__main__":
    main()
