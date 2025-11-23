# Restaurant Chat Agent

A chat agent application built with FastAPI backend and Streamlit frontend, using the official [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) for intelligent multi-agent conversations.

## Features

- **FastAPI Backend**: RESTful API with session and conversation management
- **OpenAI Agents SDK**: 
  - Automatic function calling for menu, reservations, and info
  - Intelligent agent handoffs (Menu → Reservation → Info agents)
  - Built-in conversation loop and tool execution
- **Streamlit Frontend**: Interactive chat interface
- **Comprehensive Logging**: File and console logging for both backend and frontend
- **Configuration Management**: Environment-based configuration via `.env` file

## Project Structure

```
restraunt-agent/
├── backend/
│   ├── agents/          # Agent implementations
│   ├── api/             # FastAPI routes and schemas
│   ├── core/            # Config and logging
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   └── main.py          # FastAPI entry point
├── frontend/
│   ├── core/            # Config and logging
│   ├── services/        # API client
│   └── app.py           # Streamlit app
├── logs/                # Log files (auto-generated)
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (create from .env.example)
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

### 3. Run Backend

```bash
./run_backend.sh
# Or manually:
python -m backend.main
```

The backend will start on `http://localhost:8000`

### 4. Run Frontend

In a separate terminal:

```bash
./run_frontend.sh
# Or manually:
PYTHONPATH=. streamlit run frontend/app.py
```

The frontend will open in your browser at `http://localhost:8501`

## Usage

1. Click "New Conversation" in the sidebar to start
2. Type your message in the chat input
3. The agent will respond to your queries

## API Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/session` - Create new session
- `POST /api/v1/conversation` - Create new conversation
- `POST /api/v1/chat` - Send message and get response
- `GET /api/v1/conversation/{session_id}/{conversation_id}` - Get conversation history

## Logging

Logs are stored in:
- `logs/backend/` - Backend logs
- `logs/frontend/` - Frontend logs

Logs are also printed to the console where you run the services.

## Architecture

### Agent System (OpenAI Agents SDK)

- **Main Agent**: Routes customer requests to specialized agents
- **Menu Agent**: Handles menu inquiries with `get_menu()` tool
- **Reservation Agent**: Manages bookings with `check_availability()` tool
- **Info Agent**: Provides restaurant information with hours/contact tools

The SDK automatically handles:
- Function calling and execution
- Agent handoffs based on context
- Conversation loop management
- Message history tracking

### Backend

- **Factory Pattern**: Agent and logger creation
- **Singleton Pattern**: Session manager maintains single instance
- **Service Layer**: Session and conversation management

### Frontend

- **API Client**: Centralized HTTP communication with backend
- **State Management**: Streamlit session state for conversation tracking

## Agent Examples

See `.cursor/docs/usage-examples.md` for detailed examples of:
- Creating agents with tools
- Setting up handoffs
- Adding new functionality
- Using the Runner

