from agents import function_tool
from backend.core import get_logger

logger = get_logger("tools")


@function_tool
def get_menu(category: str) -> str:
    """Get restaurant menu items by category.
    
    Args:
        category: The menu category (appetizers, mains, desserts, drinks)
    """
    logger.info(f"Getting menu for category: {category}")
    
    menus = {
        "appetizers": "Bruschetta ($8), Calamari ($12), Caesar Salad ($10)",
        "mains": "Pasta Carbonara ($18), Grilled Salmon ($24), Ribeye Steak ($32)",
        "desserts": "Tiramisu ($9), Chocolate Lava Cake ($10), Panna Cotta ($8)",
        "drinks": "Wine ($8-15/glass), Beer ($6-8), Cocktails ($12-16)"
    }
    
    result = menus.get(category.lower(), "Category not found. Available: appetizers, mains, desserts, drinks")
    logger.debug(f"Menu result: {result}")
    return result


@function_tool
def check_availability(date: str, time: str, party_size: int) -> str:
    """Check table availability for a reservation.
    
    Args:
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format (24-hour)
        party_size: Number of guests
    """
    logger.info(f"Checking availability: {date} {time} for {party_size} guests")
    
    # Simplified logic - in production, this would check a real database
    if party_size > 8:
        return f"For parties larger than 8, please call us directly at (555) 123-4567"
    
    return f"Yes, we have availability on {date} at {time} for {party_size} guests. Would you like to make a reservation?"


@function_tool
def get_restaurant_hours() -> str:
    """Get restaurant operating hours."""
    logger.info("Getting restaurant hours")
    return "Monday-Thursday: 11:00 AM - 10:00 PM, Friday-Saturday: 11:00 AM - 11:00 PM, Sunday: 12:00 PM - 9:00 PM"


@function_tool
def get_location_and_contact() -> str:
    """Get restaurant location and contact information."""
    logger.info("Getting location and contact info")
    return "123 Main Street, Downtown. Phone: (555) 123-4567. Email: info@restaurant.com"


@function_tool
def find_nearby_restaurants(location: str) -> str:
    """Find restaurant locations near the specified area.
    
    Args:
        location: City name, neighborhood, or zip code to search near
    """
    logger.info(f"Finding restaurants near: {location}")
    
    # Simulated restaurant locations
    restaurants = {
        "downtown": [
            "Main Street Location - 123 Main St (Open 11AM-11PM)",
            "Plaza Branch - 456 Plaza Ave (Open 10AM-10PM)",
            "Waterfront - 789 Harbor Blvd (Open 12PM-12AM)"
        ],
        "uptown": [
            "Uptown Square - 321 High St (Open 11AM-10PM)",
            "Park Avenue - 654 Park Ave (Open 11AM-11PM)"
        ],
        "default": [
            "Downtown Main - 123 Main St",
            "Plaza Branch - 456 Plaza Ave",
            "Uptown Square - 321 High St"
        ]
    }
    
    location_lower = location.lower()
    found_restaurants = None
    
    for key in restaurants:
        if key in location_lower:
            found_restaurants = restaurants[key]
            break
    
    if not found_restaurants:
        found_restaurants = restaurants["default"]
    
    result = f"Here are our restaurant locations near {location}:\n\n"
    result += "\n".join(f"• {r}" for r in found_restaurants)
    result += "\n\nWould you like to make a reservation at any of these locations?"
    
    return result


@function_tool
def get_special_offers() -> str:
    """Get current special offers and deals."""
    logger.info("Getting special offers")
    
    offers = """Here are our current special offers:

🎉 **Weekend Special**: 20% off all appetizers (Fri-Sun)
🍝 **Lunch Deal**: Pasta + Drink for $15 (Mon-Fri, 11AM-3PM)
🎂 **Birthday Month**: Free dessert with valid ID
👨‍👩‍👧‍👦 **Family Bundle**: 4-course meal for 4 people - $89 (Save $20!)
🥂 **Happy Hour**: 50% off drinks (Mon-Thu, 4-6PM)

All offers valid at participating locations. Some restrictions apply."""
    
    return offers

