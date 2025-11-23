from datetime import datetime
from typing import List, Dict
from backend.core import get_logger

logger = get_logger("greeting_manager")


class GreetingManager:
    
    @staticmethod
    def get_time_based_greeting() -> str:
        """Generate greeting based on time of day."""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 17:
            return "Good afternoon"
        elif 17 <= hour < 22:
            return "Good evening"
        else:
            return "Hello"
    
    @staticmethod
    def generate_initial_greeting() -> tuple[str, List[Dict[str, str]]]:
        """Generate initial greeting with quick action buttons."""
        time_greeting = GreetingManager.get_time_based_greeting()
        
        message = f"""{time_greeting}! Welcome to our restaurant chain! 🍽️

I'm here to assist you with everything you need. I can help you with:

• Finding the perfect restaurant location
• Making reservations
• Canceling or modifying bookings
• Discovering special offers and deals
• Browsing our menu

How may I assist you today?"""
        
        buttons = [
            {"label": "🏪 Find Restaurants", "action": "find_restaurants"},
            {"label": "📅 Make Reservation", "action": "make_reservation"},
            {"label": "🎁 View Offers", "action": "view_offers"},
            {"label": "📋 Browse Menu", "action": "browse_menu"}
        ]
        
        logger.info(f"Generated initial greeting with {len(buttons)} buttons")
        return message, buttons
    
    @staticmethod
    def generate_return_greeting(minutes_inactive: int) -> str:
        """Generate greeting for returning users based on inactivity."""
        time_greeting = GreetingManager.get_time_based_greeting()
        
        if minutes_inactive < 5:
            return f"{time_greeting}! I'm still here to help. What would you like to do next?"
        elif minutes_inactive < 60:
            return f"{time_greeting}! Welcome back! Ready to continue where we left off?"
        else:
            return f"{time_greeting}! Great to see you again! How can I help you today?"


greeting_manager = GreetingManager()

