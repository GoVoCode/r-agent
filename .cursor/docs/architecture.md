# Architecture Documentation

## OpenAI Agents SDK Integration

This project uses the official [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) for agent orchestration, function calling, and handoffs.

### Key SDK Components Used

1. **Agent**: Defines agent behavior with instructions, tools, and handoffs
2. **Runner**: Executes the agent loop with message history
3. **function_tool**: Decorator for creating callable tools
4. **Handoffs**: Automatic delegation to specialized agents

## Design Patterns

### Backend

#### 1. Factory Pattern (Creational)
- **Location**: `backend/agents/restaurant_agents.py`
- **Purpose**: Create specialized agents with proper configuration
- **Implementation**: `create_main_agent()`, `create_menu_agent()`, etc.
- **Benefit**: Centralized agent creation, consistent configuration

#### 2. Singleton Pattern (Creational)
- **Location**: `backend/services/session_manager.py`
- **Purpose**: Single instance of SessionManager across application
- **Implementation**: Module-level instance `session_manager`
- **Benefit**: Centralized session/conversation state management

#### 3. Factory Pattern (Creational)
- **Location**: `backend/core/logger.py`, `frontend/core/logger.py`
- **Purpose**: Create and configure loggers consistently
- **Implementation**: `LoggerFactory` class with `get_logger()` method
- **Benefit**: Centralized logger configuration, prevents duplicate handlers

#### 4. Dependency Injection
- **Location**: Throughout application
- **Purpose**: Loosely coupled components
- **Implementation**: Settings injected via `get_settings()`, loggers via `get_logger()`
- **Benefit**: Easy testing and configuration changes

### Frontend

#### 1. Service Layer Pattern
- **Location**: `frontend/services/api_client.py`
- **Purpose**: Abstraction over HTTP communication
- **Implementation**: `APIClient` encapsulates all backend API calls
- **Benefit**: Separation of concerns, easier to mock for testing

## Component Interactions

```
Frontend (Streamlit)
    ↓ HTTP
Backend API (FastAPI)
    ↓
Session Manager
    ↓
Agents SDK Runner
    ↓
Main Agent (with handoffs)
    ├─→ Menu Agent (with tools)
    ├─→ Reservation Agent (with tools)
    └─→ Info Agent (with tools)
    ↓
OpenAI API
```

## Agent Architecture

### Main Agent (Triage)
- Routes requests to specialized agents
- Handles general conversation
- Handoffs: MenuAgent, ReservationAgent, InfoAgent

### Menu Agent
- Handles menu inquiries
- Tools: `get_menu(category)`

### Reservation Agent
- Handles booking requests
- Tools: `check_availability(date, time, party_size)`, `get_restaurant_hours()`

### Info Agent
- Provides general information
- Tools: `get_restaurant_hours()`, `get_location_and_contact()`

## Session Management

- **Session**: Top-level container, created per user
- **Conversation**: Multiple conversations per session
- **Messages**: Stored in conversation with role, content, timestamp

## Logging Strategy

- Dual output: Console + File
- Separate logs for backend and frontend
- Daily log rotation via filename
- Different log levels configurable
- Structured format: `timestamp | logger | level | message`

## Configuration

- Environment-based via `.env`
- Pydantic Settings for validation
- Cached settings instance via `@lru_cache()`
- Type-safe configuration access

## Extensibility Points

1. **New Agents**: Create new agent factory functions in `restaurant_agents.py`
2. **New Tools**: Add `@function_tool` decorated functions in `tools.py`
3. **Handoffs**: Add new agents to main agent's handoff list
4. **New Endpoints**: Add routes in `backend/api/routes.py`
5. **UI Components**: Extend `frontend/app.py`

## OpenAI Agents SDK Benefits

- **Automatic Agent Loop**: No manual loop handling
- **Built-in Function Calling**: Tools are automatically invoked
- **Intelligent Handoffs**: SDK manages agent switching
- **Message History**: Seamless conversation context management
- **Structured Outputs**: Support for typed responses (if needed)
- **Tracing**: Built-in observability for debugging

