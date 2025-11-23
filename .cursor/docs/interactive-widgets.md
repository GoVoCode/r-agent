# Interactive Widgets Feature

## Overview

The reservation flow now uses interactive UI widgets (date pickers, time pickers, number inputs) instead of plain text input for better UX.

## Widget Types

### 1. Date Picker (`widget_type: "date"`)
- **Use Case**: Selecting reservation date
- **UI**: Calendar widget
- **Config**:
  - `min_date`: Earliest selectable date (default: today)
  - `max_days_ahead`: How far in future users can book (default: 60 days)

### 2. Time Picker (`widget_type: "time"`)
- **Use Case**: Selecting reservation time
- **UI**: Time input widget
- **Config**:
  - `start_time`: Restaurant opening time
  - `end_time`: Last seating time
  - `interval_minutes`: Time slot intervals (default: 30)

### 3. Number Input (`widget_type: "number"`)
- **Use Case**: Party size selection
- **UI**: Number spinner/input
- **Config**:
  - `min_value`: Minimum guests (default: 1)
  - `max_value`: Maximum guests (default: 12)
  - `default_value`: Pre-selected value (default: 2)
  - `step`: Increment step (default: 1)

### 4. Button (`widget_type: "button"`)
- **Use Case**: Quick actions (default)
- **UI**: Clickable button
- **Config**: None needed

## How It Works

### Backend Flow

1. **Agent Response Detection**
   - `WidgetManager.detect_reservation_step()` analyzes agent message
   - Looks for keywords like "what date", "what time", "how many"

2. **Widget Generation**
   - Based on detected step, creates appropriate widget config
   - Returns widget specification in response

3. **Widget Submission**
   - User interacts with widget in frontend
   - Widget data sent back as `widget_data` in chat request
   - `WidgetManager.format_widget_response()` converts to natural language

### Frontend Flow

1. **Widget Rendering**
   - Streamlit detects `widget_type` in button config
   - Renders appropriate widget (date_input, time_input, number_input)
   - Shows "Confirm" button for submission

2. **User Interaction**
   - User selects value using widget
   - Clicks confirm button
   - Widget data sent to backend

3. **Display**
   - User's selection shown as message
   - Agent processes and responds
   - Next widget appears if needed

## Reservation Flow Example

```
Agent: "What date would you like to book?"
└─ Backend detects "date" keyword
└─ Returns date picker widget

User: [Selects Dec 25, 2024 from calendar]
└─ Frontend sends: {"action": "select_date", "value": "2024-12-25"}
└─ Backend converts to: "I'd like to book for 2024-12-25"

Agent: "What time would you prefer?"
└─ Backend detects "time" keyword  
└─ Returns time picker widget

User: [Selects 7:00 PM from time picker]
└─ Frontend sends: {"action": "select_time", "value": "19:00"}
└─ Backend converts to: "at 19:00"

Agent: "How many guests will be dining?"
└─ Backend detects "party size" keyword
└─ Returns number input widget

User: [Selects 4 from number input]
└─ Frontend sends: {"action": "select_party_size", "value": 4}
└─ Backend converts to: "for 4 guests"

Agent: [Calls check_availability tool and confirms booking]
```

## Adding New Widget Types

To add a new widget type (e.g., dropdown, radio):

1. **Update Schema** (`backend/api/schemas.py`):
```python
widget_type: Literal["button", "date", "time", "number", "dropdown"]
```

2. **Add Widget Config** (`backend/agents/widget_manager.py`):
```python
elif step == "location":
    return [{
        "label": "Select Location",
        "action": "select_location",
        "widget_type": "dropdown",
        "widget_config": {
            "options": ["Downtown", "Uptown", "Waterfront"]
        }
    }]
```

3. **Add Frontend Rendering** (`frontend/app.py`):
```python
elif widget_type == "dropdown":
    selected = st.selectbox(
        button["label"],
        options=widget_config["options"],
        key=f"dropdown_{idx}"
    )
    if st.button("Confirm", key=f"confirm_dropdown_{idx}"):
        # Send widget data
```

4. **Add Detection Logic** (`widget_manager.py`):
```python
elif any(word in content_lower for word in ["which location", "select location"]):
    return "location"
```

## Benefits

- ✅ Better UX - Visual selection vs typing
- ✅ Validation - Date/time/number constraints enforced
- ✅ Less errors - No parsing ambiguous text
- ✅ Mobile friendly - Native pickers on mobile
- ✅ Accessible - Standard input widgets
- ✅ Conversation context - Widget selections stored as messages

