import os
from agents import Agent
from backend.agents.tools import (
    get_menu,
    check_availability,
    get_restaurant_hours,
    get_location_and_contact,
    find_nearby_restaurants,
    get_special_offers
)
from backend.core import get_logger, get_settings

logger = get_logger("restaurant_agents")
settings = get_settings()

os.environ["OPENAI_API_KEY"] = settings.openai_api_key


def create_menu_agent() -> Agent:
    """Create an agent specialized in menu inquiries."""
    logger.info("Creating menu agent")
    return Agent(
        name="MenuAgent",
        model=settings.openai_model,
        instructions="""You are a knowledgeable menu specialist at our restaurant.
        Help customers understand our menu offerings, explain dishes, and make recommendations.
        Be enthusiastic about the food and provide helpful descriptions.""",
        tools=[get_menu]
    )


def create_reservation_agent() -> Agent:
    """Create an agent specialized in reservations."""
    logger.info("Creating reservation agent")
    return Agent(
        name="ReservationAgent",
        model=settings.openai_model,
        instructions="""You are a reservation specialist.
        Help customers make reservations by collecting information step by step.
        
        Follow this order:
        1. Ask "What date would you like to book?" (user will use date picker)
        2. Ask "What time would you prefer?" (user will use time picker)
        3. Ask "How many guests will be dining?" (user will use number selector)
        4. Once you have all three, use check_availability tool
        5. Confirm the reservation details
        
        Be friendly and patient. If they provide info out of order, acknowledge it and ask for missing pieces.""",
        tools=[check_availability, get_restaurant_hours]
    )


def create_location_agent() -> Agent:
    """Create an agent for finding restaurant locations."""
    logger.info("Creating location agent")
    return Agent(
        name="LocationAgent",
        model=settings.openai_model,
        instructions="""You help customers find restaurant locations near them.
        Ask for their preferred area, neighborhood, or zip code.
        Use the find_nearby_restaurants tool to show available locations.
        Be enthusiastic about helping them find the perfect location.""",
        tools=[find_nearby_restaurants, get_location_and_contact]
    )


def create_offers_agent() -> Agent:
    """Create an agent for special offers and deals."""
    logger.info("Creating offers agent")
    return Agent(
        name="OffersAgent",
        model=settings.openai_model,
        instructions="""You share information about special offers, deals, and promotions.
        Be enthusiastic and help customers save money.
        Explain terms and restrictions clearly.""",
        tools=[get_special_offers]
    )


def create_info_agent() -> Agent:
    """Create an agent for general restaurant information."""
    logger.info("Creating info agent")
    return Agent(
        name="InfoAgent",
        model=settings.openai_model,
        instructions="""You provide general restaurant information including
        hours, contact details, and policies.
        Be helpful and concise.""",
        tools=[get_restaurant_hours, get_location_and_contact]
    )


def create_main_agent() -> Agent:
    """Create the main triage agent with handoffs."""
    logger.info("Creating main agent with handoffs")
    
    location_agent = create_location_agent()
    menu_agent = create_menu_agent()
    reservation_agent = create_reservation_agent()
    offers_agent = create_offers_agent()
    info_agent = create_info_agent()
    
    return Agent(
        name="MainAgent",
        model=settings.openai_model,
        instructions="""You are the main receptionist at our restaurant chain.
        Greet customers warmly and route them to the right specialist.
        
        - For finding restaurant locations or branches -> handoff to LocationAgent
        - For menu questions, dietary restrictions, or food recommendations -> handoff to MenuAgent
        - For reservations, bookings, or availability checks -> handoff to ReservationAgent
        - For special offers, deals, or promotions -> handoff to OffersAgent
        - For hours, contact info, or general policies -> handoff to InfoAgent
        
        If unsure, ask clarifying questions to route them correctly.
        Be friendly, professional, and helpful.""",
        handoffs=[location_agent, menu_agent, reservation_agent, offers_agent, info_agent]
    )

