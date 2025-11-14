# Friday 🤖

**Your Personal AI Assistant - Inspired by Tony Stark's JARVIS Successor**

Friday is a powerful, self-hosted AI assistant platform designed to be your second brain. Built on the foundation of Friday, Friday provides a seamless interface for interacting with AI models, managing knowledge, and organizing your digital life.

> *"Good morning, sir. I am Friday. I'm here to help you."*

## What is Friday?

Friday is your intelligent AI companion that helps you:

- 🧠 **Build Your Second Brain**: Store, organize, and retrieve information effortlessly
- 💬 **Chat with AI Models**: Seamlessly interact with Ollama, OpenAI, Anthropic, and more
- 📚 **Knowledge Management**: Create knowledge bases, notes, and organize your thoughts
- 🔍 **Smart Search & RAG**: Find information instantly with powerful retrieval-augmented generation
- 🎯 **Personal Workspace**: Your own AI-powered environment for productivity

## Quick Start

### Docker Compose (Recommended)

```bash
git clone https://github.com/YOUR_USERNAME/friday-second.git
cd friday-second
docker-compose up -d
```

Access Friday at: `http://localhost:3000`

### Environment Variables

Create a `.env` file:

```bash
# Required
FRIDAY_PORT=3000
WEBUI_SECRET_KEY=your-secret-key-here

# AI Provider (choose one or both)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Optional: Use local Ollama
OLLAMA_BASE_URL=http://ollama:11434
```

## Key Features ⭐

### 🧠 Second Brain Capabilities

- **Knowledge Bases**: Organize information into searchable knowledge bases
- **Notes**: Quick capture and organize thoughts
- **RAG (Retrieval Augmented Generation)**: Chat with your documents
- **Folders**: Organize chats and notes hierarchically

### 💬 AI Integration

- **Multiple Providers**: OpenAI, Anthropic Claude, Ollama, and more
- **Model Switching**: Seamlessly switch between different AI models
- **Custom Prompts**: Create and save your favorite prompts
- **Tools & Functions**: Extend capabilities with custom tools

### 🎨 User Experience

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Mode**: Easy on the eyes
- **Markdown Support**: Full Markdown and LaTeX rendering
- **Voice Input**: Hands-free interaction

### 🔒 Privacy & Control

- **Self-Hosted**: Your data stays on your server
- **Offline Capable**: Works entirely offline with local models
- **No Telemetry**: Complete privacy

## Architecture

Friday is built with:

- **Frontend**: SvelteKit + TailwindCSS
- **Backend**: FastAPI (Python)
- **Database**: SQLite (default) or PostgreSQL
- **AI Models**: Ollama (local) or Cloud APIs (OpenAI, Anthropic)

## Documentation

- **Installation Guide**: See INSTALLATION.md
- **Configuration**: See docs/configuration.md
- **Troubleshooting**: See TROUBLESHOOTING.md

## Development

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker (optional)

### Local Development

```bash
# Frontend
npm install
npm run dev

# Backend
cd backend
pip install -r requirements.txt
bash start.sh
```

## Use Cases

### Personal Knowledge Management
Build your second brain by storing articles, notes, and documents that you can instantly search and query using AI.

### Research Assistant
Upload research papers and documents, then chat with them to extract insights and summaries.

### Writing Companion
Use AI to brainstorm ideas, edit content, and improve your writing.

### Learning Tool
Create knowledge bases for subjects you're learning and quiz yourself with AI assistance.

## Inspired By

Friday is inspired by Tony Stark's AI assistant from the Marvel Cinematic Universe - an intelligent, helpful, and personable AI companion.

> *"I am Friday. I will be your AI assistant, just as JARVIS was for Mr. Stark."*

## Contributing

We welcome contributions! Please see CONTRIBUTING.md for guidelines.

## License

This project is a fork of Friday, customized for personal second brain use.

Original Friday: MIT License
Friday Customizations: MIT License

## Credits

Built on top of [Friday](https://github.com/YOUR_USERNAME/friday-second) - an excellent open-source AI interface.

Special thanks to the Friday community for creating such a powerful foundation.

---

**Friday** - Your AI Assistant, at your service. 🤖
