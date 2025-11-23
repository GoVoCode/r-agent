from fastapi import APIRouter, HTTPException
from datetime import datetime
from agents import Runner
from backend.api.schemas import (
    CreateSessionResponse,
    CreateConversationRequest,
    CreateConversationResponse,
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    HealthResponse,
    QuickActionButton
)
from backend.services import session_manager
from backend.agents import create_main_agent
from backend.agents.greeting_manager import greeting_manager
from backend.agents.widget_manager import widget_manager
from backend.core import get_logger

logger = get_logger("routes")
router = APIRouter()

main_agent = create_main_agent()

ACTION_PROMPTS = {
    "find_restaurants": "I'd like to find restaurant locations near me.",
    "make_reservation": "I want to make a reservation.",
    "view_offers": "What special offers do you have?",
    "browse_menu": "Can I see your menu?"
}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    logger.debug("Health check endpoint called")
    return HealthResponse(status="healthy", timestamp=datetime.now())


@router.post("/session", response_model=CreateSessionResponse)
async def create_session():
    logger.info("Creating new session")
    session_id = session_manager.create_session()
    return CreateSessionResponse(session_id=session_id)


@router.post("/conversation", response_model=CreateConversationResponse)
async def create_conversation(request: CreateConversationRequest):
    logger.info(f"Creating conversation in session: {request.session_id}")
    
    conversation_id = session_manager.create_conversation(request.session_id)
    if not conversation_id:
        logger.error(f"Session not found: {request.session_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    
    greeting_message, buttons = greeting_manager.generate_initial_greeting()
    
    conversation = session_manager.get_conversation(request.session_id, conversation_id)
    conversation.add_message("assistant", greeting_message, {"buttons": [b for b in buttons]})
    
    logger.info(f"Added initial greeting to conversation {conversation_id}")
    
    return CreateConversationResponse(
        conversation_id=conversation_id,
        initial_message=greeting_message,
        buttons=[QuickActionButton(**btn) for btn in buttons]
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Chat request: session={request.session_id}, conversation={request.conversation_id}")
    
    conversation = session_manager.get_conversation(
        request.session_id, 
        request.conversation_id
    )
    
    if not conversation:
        logger.error(f"Conversation not found: {request.conversation_id}")
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    user_message = request.message
    
    if request.widget_data:
        formatted_widget = widget_manager.format_widget_response(request.widget_data)
        user_message = formatted_widget
        logger.info(f"Widget data converted to: {user_message}")
    elif request.action and request.action in ACTION_PROMPTS:
        user_message = ACTION_PROMPTS[request.action]
        logger.info(f"Button action {request.action} converted to: {user_message}")
    
    conversation.add_message("user", user_message, request.metadata)
    
    try:
        all_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ]
        
        result = await Runner.run(
            main_agent,
            input=all_messages
        )
        
        response_text = result.final_output
        
        conversation.add_message("assistant", response_text)
        
        reservation_step = widget_manager.detect_reservation_step(response_text)
        response_buttons = None
        
        if reservation_step:
            widgets = widget_manager.create_reservation_widgets(reservation_step)
            response_buttons = [QuickActionButton(**w) for w in widgets]
            logger.info(f"Added {len(widgets)} widget(s) for step: {reservation_step}")
        
        logger.debug(f"Generated response for conversation {request.conversation_id}")
        
        return ChatResponse(
            response=response_text,
            conversation_id=request.conversation_id,
            timestamp=datetime.now(),
            buttons=response_buttons
        )
        
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@router.get("/conversation/{session_id}/{conversation_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(session_id: str, conversation_id: str):
    logger.info(f"Fetching conversation history: {conversation_id}")
    
    conversation = session_manager.get_conversation(session_id, conversation_id)
    
    if not conversation:
        logger.error(f"Conversation not found: {conversation_id}")
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = [
        {
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
            "metadata": msg.metadata
        }
        for msg in conversation.messages
    ]
    
    return ConversationHistoryResponse(
        conversation_id=conversation_id,
        messages=messages
    )

