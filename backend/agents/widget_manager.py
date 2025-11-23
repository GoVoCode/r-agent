from typing import List, Dict, Any
from backend.core import get_logger

logger = get_logger("widget_manager")


class WidgetManager:
    
    @staticmethod
    def create_reservation_widgets(step: str) -> List[Dict[str, Any]]:
        """Create interactive widgets based on reservation step."""
        
        if step == "date":
            return [{
                "label": "Select Date",
                "action": "select_date",
                "widget_type": "date",
                "widget_config": {
                    "min_date": "today",
                    "max_days_ahead": 60
                }
            }]
        
        elif step == "time":
            return [{
                "label": "Select Time",
                "action": "select_time",
                "widget_type": "time",
                "widget_config": {
                    "start_time": "11:00",
                    "end_time": "22:00",
                    "interval_minutes": 30
                }
            }]
        
        elif step == "party_size":
            return [{
                "label": "Number of Guests",
                "action": "select_party_size",
                "widget_type": "number",
                "widget_config": {
                    "min_value": 1,
                    "max_value": 12,
                    "default_value": 2,
                    "step": 1
                }
            }]
        
        return []
    
    @staticmethod
    def detect_reservation_step(message_content: str) -> str:
        """Detect which reservation step we're at based on agent message."""
        content_lower = message_content.lower()
        
        if any(word in content_lower for word in ["what date", "which date", "when would you", "select a date"]):
            return "date"
        elif any(word in content_lower for word in ["what time", "which time", "prefer time", "select a time"]):
            return "time"
        elif any(word in content_lower for word in ["how many", "party size", "number of guests", "how many people"]):
            return "party_size"
        
        return None
    
    @staticmethod
    def format_widget_response(widget_data: Dict[str, Any]) -> str:
        """Format widget data into natural language."""
        action = widget_data.get("action")
        value = widget_data.get("value")
        
        if action == "select_date":
            return f"I'd like to book for {value}"
        elif action == "select_time":
            return f"at {value}"
        elif action == "select_party_size":
            return f"for {value} guests"
        
        return str(value)


widget_manager = WidgetManager()

