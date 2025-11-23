# Usage Examples - OpenAI Agents SDK

This document shows how the OpenAI Agents SDK is used in this project.

## Basic Agent with Tools

```python
from agents import Agent, function_tool

@function_tool
def get_menu(category: str) -> str:
    """Get restaurant menu items by category."""
    return f"Menu items for {category}..."

menu_agent = Agent(
    name="MenuAgent",
    instructions="You help with menu inquiries.",
    tools=[get_menu]
)
```

## Agent with Handoffs

```python
from agents import Agent, Runner

# Create specialized agents
menu_agent = Agent(name="MenuAgent", instructions="...", tools=[get_menu])
booking_agent = Agent(name="BookingAgent", instructions="...", tools=[check_availability])

# Main agent with handoffs
main_agent = Agent(
    name="MainAgent",
    instructions="Route to specialists based on user needs.",
    handoffs=[menu_agent, booking_agent]
)

# Run with message history
result = await Runner.run(
    main_agent,
    input="What's on the menu?",
    message_history=[
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help?"}
    ]
)
print(result.final_output)
```

## How It Works in This Project

### 1. Agent Creation (`backend/agents/restaurant_agents.py`)

```python
def create_main_agent() -> Agent:
    menu_agent = create_menu_agent()
    reservation_agent = create_reservation_agent()
    info_agent = create_info_agent()
    
    return Agent(
        name="MainAgent",
        instructions="Greet customers and route to specialists...",
        handoffs=[menu_agent, reservation_agent, info_agent]
    )
```

### 2. Running Agent (`backend/api/routes.py`)

```python
from agents import Runner

# In the chat endpoint
result = await Runner.run(
    main_agent,
    input=user_message,
    message_history=conversation_history
)

response_text = result.final_output
```

## The Agent Loop (Handled by SDK)

The SDK automatically:

1. **Calls the LLM** with agent instructions and message history
2. **Executes tools** if the LLM decides to use them
3. **Handles handoffs** by switching to specialized agents
4. **Returns final output** when the agent provides a complete response

You don't need to manually:
- Parse tool calls
- Execute functions
- Manage agent switching
- Handle the conversation loop

## Adding New Functionality

### Add a New Tool

```python
# In backend/agents/tools.py

@function_tool
def get_special_offers() -> str:
    """Get current restaurant special offers."""
    return "Today's special: 20% off all appetizers!"

# Add to appropriate agent in restaurant_agents.py
def create_menu_agent() -> Agent:
    return Agent(
        name="MenuAgent",
        instructions="...",
        tools=[get_menu, get_special_offers]  # Add new tool
    )
```

### Add a New Agent

```python
# In backend/agents/restaurant_agents.py

def create_delivery_agent() -> Agent:
    return Agent(
        name="DeliveryAgent",
        instructions="Handle delivery inquiries and orders.",
        tools=[check_delivery_zone, estimate_delivery_time]
    )

# Add to main agent handoffs
def create_main_agent() -> Agent:
    delivery_agent = create_delivery_agent()
    
    return Agent(
        name="MainAgent",
        instructions="... For delivery -> handoff to DeliveryAgent",
        handoffs=[..., delivery_agent]  # Add to handoffs
    )
```

## Environment Setup

The SDK automatically uses the `OPENAI_API_KEY` from your environment. Set it in `.env`:

```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini  # or gpt-4o, gpt-4, etc.
```

## References

- [OpenAI Agents SDK GitHub](https://github.com/openai/openai-agents-python)
- [SDK Documentation](https://openai.github.io/openai-agents-python/)

