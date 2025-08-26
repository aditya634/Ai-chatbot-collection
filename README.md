# 🤖 AI Chatbot Collection

A comprehensive collection of AI-powered chatbots built with Python, featuring terminal-based and web-based interfaces with different AI backends including Google Gemini and Ollama local models.

## 📋 Project Overview

This repository contains three distinct chatbot implementations:

1. **🕉️ Indian God Chatbot** - Terminal-based chatbot using Google Gemini API
2. **💬 Local Host Chatbot** - Streamlit web app using local Ollama models  
3. **🕷️ Web Crawler & Scraper Bot** - Advanced web scraping chatbot with crawling capabilities

## 🚀 Features

### Terminal Chatbot (ChatBot_api.py)
- **Google Gemini Integration**: Uses Google's Gemini-2.5-flash model
- **Terminal Interface**: Simple command-line interaction
- **Conversational AI**: Natural language processing capabilities
- **Exit Command**: Type 'bye' to exit gracefully

### Local Host Chatbot (ChatBot_Local_Host.py) 
- **Local AI Models**: Powered by Ollama (Qwen2.5:7b-instruct)
- **Streamlit Web UI**: Modern, responsive web interface
- **Real-time Chat**: Interactive chat bubbles and smooth UX
- **Session Management**: Maintains conversation history
- **Customizable Persona**: Configurable system prompts

### Web Crawler & Scraper Bot (ChatBot_scraper_app.py)
- **🔗 Single Page Scraping**: Extract and summarize individual web pages
- **🕷️ Multi-Page Crawling**: Intelligently crawl entire websites (up to 5 pages)
- **🤖 AI-Powered Analysis**: Comprehensive content summarization using local AI
- **🎯 Smart Detection**: Automatically detects URLs vs. general questions
- **⚙️ Respectful Crawling**: Built-in delays and domain restrictions
- **📊 Progress Tracking**: Real-time crawling progress indicators
- **🛡️ Error Handling**: Graceful handling of failed requests and timeouts

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running (for local models)
- Google API key (for Gemini chatbot)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-chatbot-collection.git
cd ai-chatbot-collection
```

### 2. Create Virtual Environment
```bash
python -m venv chatbot_env
# Windows
chatbot_env\Scripts\activate
# macOS/Linux  
source chatbot_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup AI Models

#### For Google Gemini (Terminal Chatbot):
1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Replace `YOUR_API_KEY` in `ChatBot_api.py` with your actual key

#### For Ollama (Local Chatbots):
1. Install [Ollama](https://ollama.com/download)
2. Install the Qwen2.5 model:
```bash
ollama pull qwen2.5:7b-instruct
```
3. Start Ollama server:
```bash
ollama serve
```

## 🎯 Usage

### Terminal Chatbot
```bash
python ChatBot_api.py
```
- Type your messages and press Enter
- Type 'bye' to exit

### Local Host Chatbot  
```bash
streamlit run ChatBot_Local_Host.py
```
- Open http://localhost:8501 in your browser
- Chat using the web interface

### Web Crawler & Scraper Bot
```bash
streamlit run ChatBot_scraper_app.py  
```
- Open http://localhost:8501 in your browser

#### Usage Examples:
**Single Page Scraping:**
```
https://news.ycombinator.com
https://en.wikipedia.org/wiki/Machine_learning
```

**Multi-Page Crawling:**
```
crawl https://docs.python.org
https://example.com multiple pages
analyze entire site https://flask.palletsprojects.com
```

**General Questions:**
```
What is artificial intelligence?
Explain quantum computing
```

## 🏗️ Project Structure

```
ChatBot/
├── ChatBot_api.py              # Terminal chatbot with Gemini API
├── ChatBot_Local_Host.py       # Streamlit app with local Ollama
├── ChatBot_scraper_app.py      # Web scraper/crawler chatbot
├── chatbot_env/               # Virtual environment
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── LICENSE                  # MIT License
```

## 🔧 Technical Architecture

### Web Scraper Bot Architecture:
```
User Input → URL Detection → Mode Selection
     ↓              ↓              ↓
Single Page ←→ Crawl Mode ←→ General Q&A
     ↓              ↓              ↓
BeautifulSoup → BFS Crawling → Direct AI
     ↓              ↓              ↓
Content Clean → Multi-page → Response
     ↓              ↓              ↓
AI Summary ←→ Combined Analysis ←→ Display
```

### Key Components:
- **URL Detection**: Regex-based URL extraction
- **Content Extraction**: BeautifulSoup HTML parsing
- **Smart Crawling**: Queue-based BFS algorithm
- **AI Integration**: Ollama local model API
- **UI Components**: Streamlit reactive interface

## 📦 Dependencies

```txt
streamlit>=1.28.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
google-generativeai>=0.3.0
urllib3>=2.0.0
```

## ⚙️ Configuration

### Ollama Model Configuration:
- **Model**: qwen2.5:7b-instruct
- **API Endpoint**: http://localhost:11434/api/generate
- **Max Pages (Crawling)**: 5 pages per request
- **Crawl Delay**: 1 second between requests
- **Content Limit**: 8000 characters per page (single), 3000 per page (crawl)

### Customization Options:
- **System Prompts**: Modify chatbot personality in each file
- **Crawl Limits**: Adjust `max_pages` parameter in `crawl_website()`
- **UI Styling**: Customize CSS in Streamlit markdown sections
- **Model Selection**: Change `MODEL_NAME` to use different Ollama models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛡️ Security & Privacy

- **API Keys**: Never commit API keys to version control
- **Rate Limiting**: Built-in delays for respectful web crawling
- **Error Handling**: Comprehensive exception management
- **Content Filtering**: Automatic removal of scripts and ads

## 📊 Performance

### Benchmarks:
- **Single Page Scraping**: ~2-3 seconds average
- **Multi-Page Crawling**: ~10-15 seconds (5 pages)
- **AI Response Time**: ~1-5 seconds (depends on content length)
- **Memory Usage**: ~50-100MB (excluding AI model)

## 🔍 Troubleshooting

### Common Issues:

**Ollama Connection Error:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

**Model Not Found:**
```bash
# Install the required model
ollama pull qwen2.5:7b-instruct
```

**Web Scraping Blocked:**
- Some sites block automated requests
- User-Agent headers help mimic real browsers
- Respect robots.txt and rate limits

## 📞 Support

For issues, questions, or contributions:
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/ai-chatbot-collection/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/yourusername/ai-chatbot-collection/discussions)

## 🌟 Acknowledgments

- **Ollama** for local AI model serving
- **Google** for Gemini API access
- **Streamlit** for the amazing web framework
- **BeautifulSoup** for HTML parsing capabilities

---

**Made with ❤️ and Python** | **Powered by AI** 🤖
