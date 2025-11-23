# Agent-Initiated Conversation Feature

## Overview

The agent now initiates conversations with personalized greetings and interactive quick-action buttons.

## Features

### 1. Time-Based Personalization
- **Morning (5am-12pm)**: "Good morning!"
- **Afternoon (12pm-5pm)**: "Good afternoon!"
- **Evening (5pm-10pm)**: "Good evening!"
- **Night (10pm-5am)**: "Hello!"

### 2. Initial Greeting
When a user creates a new conversation, the agent automatically sends:
- Personalized time-based greeting
- Welcome message explaining capabilities
- Quick action buttons for common tasks

### 3. Quick Action Buttons
Four main action buttons are displayed:
- 🏪 **Find Restaurants** - Locate nearby restaurant locations
- 📅 **Make Reservation** - Book a table
- 🎁 **View Offers** - Check special deals
- 📋 **Browse Menu** - See menu items

### 4. Smart Return Greetings
Based on inactivity duration:
- **< 5 minutes**: "I'm still here to help. What would you like to do next?"
- **5-60 minutes**: "Welcome back! Ready to continue where we left off?"
- **> 60 minutes**: "Great to see you again! How can I help you today?"

## Implementation

### Backend Components

**`GreetingManager`** (`backend/agents/greeting_manager.py`)
- Generates time-based greetings
- Creates button configurations
- Manages return user greetings

**`Conversation` Model** (`backend/models/session.py`)
- Tracks `last_activity` timestamp
- Provides `is_inactive()` method

**API Endpoints** (`backend/api/routes.py`)
- `/conversation` - Returns initial greeting with buttons
- `/chat` - Accepts `action` parameter for button clicks

### Frontend Components

**Streamlit UI** (`frontend/app.py`)
- Displays greeting automatically on conversation creation
- Renders interactive buttons below assistant messages
- Handles button clicks by sending action to backend

## Flow

1. User clicks "New Conversation"
2. Backend creates conversation and generates greeting
3. Frontend receives greeting + buttons
4. Greeting displayed as first message
5. User clicks button or types message
6. Backend processes (converts button action to text prompt)
7. Agent responds through normal flow

## Button Actions

Buttons are converted to natural language prompts:

```python
ACTION_PROMPTS = {
    "find_restaurants": "I'd like to find restaurant locations near me.",
    "make_reservation": "I want to make a reservation.",
    "view_offers": "What special offers do you have?",
    "browse_menu": "Can I see your menu?"
}
```

This maintains conversation context while providing UI convenience.

