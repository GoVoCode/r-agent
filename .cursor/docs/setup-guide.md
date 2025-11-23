# Setup Guide

## Prerequisites

- Python 3.10+
- OpenAI API Key

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `agents==0.6.1` - OpenAI Agents SDK
- `fastapi` - Backend framework
- `streamlit` - Frontend framework
- Other required packages

### 2. Configure Environment

Copy the example environment file:

```bash
cp env.example .env
```

Edit `.env` and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-proj-...  # Your actual OpenAI API key
OPENAI_MODEL=gpt-4o-mini    # or gpt-4o, gpt-4, etc.

BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
LOG_LEVEL=DEBUG

FRONTEND_HOST=localhost
FRONTEND_PORT=8501
BACKEND_API_URL=http://localhost:8000
```

### 3. Run the Backend

From the project root:

```bash
./run_backend.sh
```

Or manually:

```bash
python -m backend.main
```

Expected output:
```
2024-XX-XX XX:XX:XX | session_manager | INFO | SessionManager initialized
2024-XX-XX XX:XX:XX | restaurant_agents | INFO | Creating main agent with handoffs
2024-XX-XX XX:XX:XX | main | INFO | FastAPI application initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Run the Frontend

In a **new terminal**, from the project root:

```bash
./run_frontend.sh
```

Or manually:

```bash
PYTHONPATH=. streamlit run frontend/app.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### 5. Test the Application

1. Open browser to http://localhost:8501
2. Click "Check Backend Status" - should show "✅ Backend is healthy"
3. Click "🆕 New Conversation"
4. Try these test messages:
   - "What's on your menu?" (triggers MenuAgent with get_menu tool)
   - "Do you have availability on Friday at 7pm for 4 people?" (triggers ReservationAgent)
   - "What are your hours?" (triggers InfoAgent)

## Troubleshooting

### Import Error: No module named 'agents'

```bash
pip install agents==0.6.1
```

### Import Error: No module named 'frontend'

Make sure you're running from the project root with PYTHONPATH set:

```bash
cd /Users/gurvinderyadav/Documents/restraunt-agent
PYTHONPATH=. streamlit run frontend/app.py
```

Or use the provided script:

```bash
./run_frontend.sh
```

### OpenAI API Key Error

Make sure your `.env` file has a valid `OPENAI_API_KEY`:

```bash
# Check if .env exists
ls -la .env

# Make sure it contains your key
cat .env | grep OPENAI_API_KEY
```

### Backend Connection Error in Frontend

1. Check backend is running: `curl http://localhost:8000/api/v1/health`
2. Check `BACKEND_API_URL` in `.env` matches backend address
3. Check no firewall blocking port 8000

## Verifying Installation

Test the agents SDK is working:

```python
# test_agents.py
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="Test",
    instructions="You are helpful."
)

async def main():
    result = await Runner.run(agent, input="Say hello")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python test_agents.py
# Should output a greeting
```

## Next Steps

- Read `.cursor/docs/usage-examples.md` for agent customization
- Read `.cursor/docs/architecture.md` for system design
- Explore `backend/agents/tools.py` to add new tools
- Explore `backend/agents/restaurant_agents.py` to add new agents

