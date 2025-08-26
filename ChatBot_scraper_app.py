import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time
from collections import deque

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b-instruct"

SCRAPER_SYSTEM_PROMPT = (
    "You are an intelligent web content analyzer and summarizer. "
    "Your task is to analyze web content (single page or multiple pages) and create comprehensive, well-structured summaries. "
    "When given website content, you should:\n\n"
    "1. Identify the main topic and key themes across all pages\n"
    "2. Extract important information, statistics, and facts\n"
    "3. Organize the summary in a clear, hierarchical format\n"
    "4. Highlight any significant insights or conclusions\n"
    "5. If multiple pages were crawled, mention the breadth of content covered\n"
    "6. Mention the source website(s) for reference\n\n"
    "For crawled content, provide an overview of the site structure and main sections. "
    "Provide summaries that are informative, accurate, and easy to understand. "
    "If the content is technical, explain complex concepts in simpler terms."
)

st.set_page_config(page_title="Web Scraper Chatbot", page_icon="🕷️")
st.markdown(
    "<h1 style='text-align: center; color: #1f77b4;'>🕷️ Web Crawler & Scraper Bot 🕷️</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #666;'>Paste a URL to scrape single pages, or add 'crawl' to analyze entire websites!</p>",
    unsafe_allow_html=True,
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

def is_valid_url(url):
    """Check if the provided string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def scrape_website(url):
    """Scrape content from the given URL"""
    try:
        # Add headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make request with timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get title
        title = soup.title.string if soup.title else "No title found"
        
        # Extract main content (prioritize article, main, or div with content)
        content_tags = soup.find_all(['article', 'main', 'div', 'section', 'p', 'h1', 'h2', 'h3'])
        
        # Extract text from relevant tags
        text_content = []
        for tag in content_tags:
            text = tag.get_text(strip=True)
            if len(text) > 50:  # Only include substantial text blocks
                text_content.append(text)
        
        # Join and clean the content
        full_content = ' '.join(text_content)
        # Remove extra whitespaces and newlines
        full_content = re.sub(r'\s+', ' ', full_content).strip()
        
        return {
            'title': title.strip(),
            'content': full_content[:8000],  # Limit content to prevent token overflow
            'url': url,
            'success': True
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'error': f"Failed to fetch the website: {str(e)}",
            'success': False
        }
    except Exception as e:
        return {
            'error': f"Error processing the website: {str(e)}",
            'success': False
        }

def get_internal_links(url, soup, max_links=10):
    """Extract internal links from the current page"""
    base_domain = urlparse(url).netloc
    internal_links = set()
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        
        # Convert relative URLs to absolute
        absolute_url = urljoin(url, href)
        parsed_url = urlparse(absolute_url)
        
        # Check if it's an internal link (same domain)
        if parsed_url.netloc == base_domain and parsed_url.scheme in ['http', 'https']:
            # Avoid fragments and query parameters for cleaner crawling
            clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            internal_links.add(clean_url)
            
            if len(internal_links) >= max_links:
                break
    
    return list(internal_links)

def crawl_website(start_url, max_pages=5, delay=1):
    """Crawl multiple pages from a website"""
    try:
        visited = set()
        to_visit = deque([start_url])
        crawled_data = []
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        progress_placeholder = st.empty()
        
        while to_visit and len(crawled_data) < max_pages:
            current_url = to_visit.popleft()
            
            if current_url in visited:
                continue
                
            visited.add(current_url)
            progress_placeholder.text(f"🕷️ Crawling page {len(crawled_data) + 1}/{max_pages}: {current_url}")
            
            try:
                response = requests.get(current_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove unwanted elements
                for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                    script.decompose()
                
                # Get title
                title = soup.title.string if soup.title else "No title found"
                
                # Extract content
                content_tags = soup.find_all(['article', 'main', 'div', 'section', 'p', 'h1', 'h2', 'h3'])
                text_content = []
                
                for tag in content_tags:
                    text = tag.get_text(strip=True)
                    if len(text) > 30:
                        text_content.append(text)
                
                full_content = ' '.join(text_content)
                full_content = re.sub(r'\s+', ' ', full_content).strip()
                
                if full_content:  # Only add pages with content
                    crawled_data.append({
                        'url': current_url,
                        'title': title.strip(),
                        'content': full_content[:3000],  # Limit per page to manage total size
                    })
                
                # Get internal links for further crawling
                if len(crawled_data) < max_pages:
                    internal_links = get_internal_links(current_url, soup, max_links=5)
                    for link in internal_links:
                        if link not in visited:
                            to_visit.append(link)
                
                # Respectful delay between requests
                time.sleep(delay)
                
            except Exception as e:
                st.warning(f"Failed to crawl {current_url}: {str(e)}")
                continue
        
        progress_placeholder.empty()
        
        if crawled_data:
            return {
                'success': True,
                'pages_crawled': len(crawled_data),
                'data': crawled_data,
                'start_url': start_url
            }
        else:
            return {
                'success': False,
                'error': "No content could be extracted from the website"
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': f"Crawling failed: {str(e)}"
        }

def get_ollama_response(prompt):
    """Get response from Ollama model"""
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{SCRAPER_SYSTEM_PROMPT}\n\nUser Query: {prompt}\n\nAI Response:",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"].strip()

def process_user_input(user_input):
    """Process user input - URL with crawl options or regular question"""
    # Check if input contains a URL
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', user_input)
    
    if urls:
        url = urls[0]  # Take the first URL found
        
        # Check if user wants to crawl (keywords: crawl, multiple pages, site map, etc.)
        crawl_keywords = ['crawl', 'multiple pages', 'entire site', 'all pages', 'site map', 'deep dive', 'full site']
        should_crawl = any(keyword in user_input.lower() for keyword in crawl_keywords)
        
        if should_crawl:
            # Crawl multiple pages
            st.info("🕷️ **Crawl Mode Activated** - Extracting content from multiple pages...")
            crawled_data = crawl_website(url, max_pages=5, delay=1)
            
            if crawled_data['success']:
                # Combine all page content
                all_content = []
                page_titles = []
                
                for page in crawled_data['data']:
                    page_titles.append(f"• {page['title']} ({page['url']})")
                    all_content.append(f"Page: {page['title']}\nURL: {page['url']}\nContent: {page['content']}\n---")
                
                combined_content = '\n\n'.join(all_content)
                pages_info = '\n'.join(page_titles)
                
                prompt = f"""I crawled {crawled_data['pages_crawled']} pages from the website. Please analyze and provide a comprehensive summary:

Starting URL: {crawled_data['start_url']}

Pages Crawled:
{pages_info}

Combined Content:
{combined_content[:12000]}  # Limit total content

Please provide a comprehensive analysis covering:
1. Overall website theme and purpose
2. Main sections and topics covered
3. Key insights and information
4. Site structure and organization"""
                
                return get_ollama_response(prompt)
            else:
                return f"❌ Error during crawling: {crawled_data['error']}"
        
        else:
            # Single page scraping
            with st.spinner(f"🕷️ Scraping content from {url}..."):
                scraped_data = scrape_website(url)
            
            if scraped_data['success']:
                prompt = f"""Please analyze and summarize the following website content:

URL: {scraped_data['url']}
Title: {scraped_data['title']}

Content:
{scraped_data['content']}

Please provide a comprehensive summary of this website's content."""
                
                return get_ollama_response(prompt)
            else:
                return f"❌ Error scraping website: {scraped_data['error']}"
    else:
        # Regular question - no URL detected
        return get_ollama_response(user_input)

def send_message():
    user_input = st.session_state.user_input
    if user_input.strip():
        bot_response = process_user_input(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_response))
        st.session_state.clear_input = True

def on_input_change():
    user_input = st.session_state.user_input
    if user_input.strip():
        send_message()

# Chat display area
chat_placeholder = st.container()
with chat_placeholder:
    st.markdown(
        """
        <style>
        .user-bubble {
            background-color: #e3f2fd;
            color: #0d47a1;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            margin-left: 50px;
            text-align: right;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .bot-bubble {
            background-color: #f3e5f5;
            color: #4a148c;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            margin-right: 50px;
            text-align: left;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-container {
            max-height: 600px;
            overflow-y: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    if not st.session_state.chat_history:
        st.markdown(
            "<div style='text-align: center; color: #666; padding: 20px;'>"
            "👋 Hi! I can scrape single pages or crawl entire websites!<br>"
            "🔗 <b>Single page:</b> Just paste a URL<br>"
            "🕷️ <b>Crawl mode:</b> Add 'crawl' keyword with your URL<br>"
            "💬 You can also ask me general questions!</div>",
            unsafe_allow_html=True
        )
    
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"<div class='user-bubble'><b>🧑‍💻 You:</b> {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'><b>🤖 AI:</b> {message}</div>", unsafe_allow_html=True)

st.markdown("---")

# Instructions
with st.expander("📋 How to use"):
    st.markdown("""
    **🔗 For Single Page Scraping:**
    - Paste any website URL (e.g., https://example.com)
    - The bot will scrape and summarize that page only
    
    **🕷️ For Website Crawling (Multiple Pages):**
    - Add crawl keywords like: "crawl", "multiple pages", "entire site", "all pages"
    - Examples:
      - `Crawl https://example.com`
      - `https://example.com multiple pages`
      - `Analyze entire site https://example.com`
    
    **💬 For General Questions:**
    - Ask any question without a URL
    - Get AI-powered responses
    
    **📝 Examples:**
    - `https://news.ycombinator.com` (single page)
    - `Crawl https://docs.python.org` (multiple pages)
    - `What is machine learning?` (general question)
    - `https://en.wikipedia.org/wiki/AI entire site` (crawl mode)
    
    **⚙️ Crawling Features:**
    - Crawls up to 5 pages per request
    - 1-second delay between requests (respectful crawling)
    - Follows internal links only
    - Provides comprehensive site analysis
    """)

col1, col2 = st.columns([5, 1])

# Clear input if flag is set
if st.session_state.clear_input:
    st.session_state.user_input = ""
    st.session_state.clear_input = False

with col1:
    user_input = st.text_input(
        "Enter a website URL or ask a question...",
        key="user_input",
        label_visibility="collapsed",
        placeholder="🔗 URL or 'crawl https://example.com' or ask a question...",
        on_change=on_input_change
    )
with col2:
    if st.button("🚀 Send", use_container_width=True):
        if user_input.strip():
            send_message()
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 12px;'>"
    "🕷️ Web Crawler & Scraper Bot - Powered by Ollama, BeautifulSoup & Smart Crawling"
    "</div>",
    unsafe_allow_html=True
)
