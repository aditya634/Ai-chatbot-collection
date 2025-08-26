# 🚀 Quick Start Guide

Get your AI chatbots running in minutes!

## ⚡ Super Quick Setup (Windows)

```bash
# 1. Clone and setup
git clone <your-repo-url>
cd ai-chatbot-collection
python setup.py

# 2. Setup Ollama (for local chatbots)
# Download from: https://ollama.com/download
ollama pull qwen2.5:7b-instruct
ollama serve

# 3. Run your preferred chatbot
chatbot_env\Scripts\streamlit run ChatBot_scraper_app.py
```

## 🎯 Which Chatbot Should I Use?

### 🕷️ **Web Scraper Bot** (Recommended)
**Best for**: Analyzing websites, research, content summary
```bash
streamlit run ChatBot_scraper_app.py
```
**Try**: `crawl https://docs.python.org`

### 💬 **Local Host Chatbot** 
**Best for**: General conversations, privacy-focused AI
```bash
streamlit run ChatBot_Local_Host.py
```

### 🕉️ **Terminal Chatbot**
**Best for**: Quick CLI interactions, API testing
```bash
python ChatBot_api.py
```

## 🛠️ Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] Ollama installed and running (for local bots)
- [ ] Google API key (for terminal bot)

## 🎉 That's It!

Your chatbots are ready to use! Check the main README.md for detailed documentation.

---
**Need help?** Open an issue on GitHub! 🤝
